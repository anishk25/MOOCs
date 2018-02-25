package block_chain;


import java.util.*;

public class TxHandler {

    private UTXOPool utxoPool;
    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
    public TxHandler(UTXOPool utxoPool) {
        this.utxoPool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if:
     * (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
     * (2) the signatures on each input of {@code tx} are valid, 
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        return areInputsValid(tx) &&
                checkDoubleSpending(tx) &&
                areOutputsPositive(tx) &&
                isTransactionBalanced(tx);
    }

    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        Set<Transaction> remainingTransactions = new HashSet<>(Arrays.asList(possibleTxs));
        List<TransactionNode> rootNodes = getRootNodes(possibleTxs, remainingTransactions);
        constructTransactionGraph(rootNodes, remainingTransactions);
        return getValidTransactionsFromGraph(rootNodes);
    }

    private List<TransactionNode> getRootNodes(Transaction[] possibleTxs, Set<Transaction> remainingTransactions) {
        // a root node contains a transaction whose  inputs are already
        // in the existing UTXO pool
        List<TransactionNode> rootNodes = new ArrayList<>();

        for (Transaction tx : possibleTxs) {
            boolean isRoot = true;
            for (Transaction.Input input : tx.getInputs()) {
                if (!isInUTXOPool(input)) {
                    isRoot = false;
                    break;
                }
            }

            if (isRoot) {
                rootNodes.add(new TransactionNode(tx, new ArrayList<>()));
                remainingTransactions.remove(tx);
            }
        }

        return rootNodes;
    }

    private void constructTransactionGraph(List<TransactionNode> rootNodes, Set<Transaction> nonRootTransactions) {
        Queue<TransactionNode> nodesQueue = new LinkedList<>(rootNodes);
        Set<Integer> visited = new HashSet<>();

        Map<Integer, TransactionNode> nodeMap = new HashMap<>();
        for (TransactionNode node : rootNodes) {
            nodeMap.put(getTransacationHashCode(node.tx), node);
        }


        while(!nodesQueue.isEmpty()) {
            TransactionNode currNode = nodesQueue.poll();
            visited.add(getTransacationHashCode(currNode.tx));

            for(Transaction tx : nonRootTransactions) {
                int hash = getTransacationHashCode(tx);
                if (visited.contains(hash)) {
                    continue;
                }

                if (isChild(tx, currNode.tx)) {
                    TransactionNode newNode;
                    if (nodeMap.containsKey(hash)) {
                        newNode = nodeMap.get(hash);
                    } else {
                        newNode = new TransactionNode(tx, new ArrayList<>());
                        nodeMap.put(hash, newNode);
                    }
                    currNode.children.add(newNode);
                    nodesQueue.add(newNode);
                }
            }
        }
    }

    private boolean isChild(Transaction child, Transaction parent) {
        for (Transaction.Input input : child.getInputs()) {
            if (Arrays.equals(input.prevTxHash, parent.getHash())) {
                return true;
            }
        }
        return false;
    }

    private Transaction [] getValidTransactionsFromGraph(List<TransactionNode> rootNodes) {

        Queue<TransactionNode> queue = new LinkedList<>(rootNodes);
        ArrayList<Transaction> validTransactions = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();

        while (!queue.isEmpty()) {
            TransactionNode currNode = queue.poll();
            visited.add(getTransacationHashCode(currNode.tx));
            if (isValidTx(currNode.tx)) {
                ArrayList<Transaction.Output> outputs = currNode.tx.getOutputs();

                for (Transaction.Input input : currNode.tx.getInputs()) {
                    utxoPool.removeUTXO(getUTXOFromInput(input));
                }

                for (int i = 0; i < outputs.size(); i++) {
                    utxoPool.addUTXO(new UTXO(currNode.tx.getHash(), i), outputs.get(i));
                }
                validTransactions.add(currNode.tx);

                for (TransactionNode child : currNode.children) {
                    if (!visited.contains(getTransacationHashCode(child.tx))) {
                        queue.add(child);
                    }
                }
            }
        }
        return validTransactions.toArray(new Transaction[validTransactions.size()]);
    }


    private boolean areInputsValid (Transaction tx) {
        for (int i = 0; i < tx.getInputs().size(); i++) {
            boolean valid = isInUTXOPool(tx.getInput(i)) && hasValidSignature(i, tx);
            if (!valid) {
                return false;
            }
        }
        return true;
    }

    private boolean checkDoubleSpending(Transaction tx) {
        Set<UTXO> coveredUTXOs = new HashSet<>();
        for (Transaction.Input input : tx.getInputs()) {
            UTXO utxo = getUTXOFromInput(input);
            if (coveredUTXOs.contains(utxo)) {
                return false;
            }
            coveredUTXOs.add(utxo);
        }
        return true;
    }

    private boolean areOutputsPositive(Transaction tx) {
        for (Transaction.Output output : tx.getOutputs()) {
            if (output.value < 0) {
                return false;
            }
        }
        return true;
    }

    private boolean isTransactionBalanced(Transaction tx) {
        double inputValue = 0;
        for (Transaction.Input input: tx.getInputs()) {
            UTXO utxo = getUTXOFromInput(input);
            inputValue += utxoPool.getTxOutput(utxo).value;
        }

        for (Transaction.Output output : tx.getOutputs()) {
            inputValue -= output.value;
            if (inputValue < 0) {
                return false;
            }
        }

        return true;
    }

    private boolean isInUTXOPool(Transaction.Input input) {
        UTXO utxo = getUTXOFromInput(input);
        return utxoPool.contains(utxo);
    }

    private boolean hasValidSignature(int inputIndex, Transaction tx) {
        Transaction.Input input = tx.getInput(inputIndex);
        UTXO utxo = new UTXO(input.prevTxHash, input.outputIndex);
        Transaction.Output output = utxoPool.getTxOutput(utxo);
        return Crypto.verifySignature(output.address, tx.getRawDataToSign(inputIndex), input.signature);
    }

    private UTXO getUTXOFromInput(Transaction.Input input) {
        return new UTXO(input.prevTxHash, input.outputIndex);
    }


    private int getTransacationHashCode(Transaction transaction) {
        return Arrays.hashCode(transaction.getHash());
    }

    private class TransactionNode {
        private final Transaction tx;
        private final List<TransactionNode> children;

        private TransactionNode(Transaction tx, List<TransactionNode> children) {
            this.tx = tx;
            this.children = children;
        }
    }
}
