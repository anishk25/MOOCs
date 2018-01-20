package consensus;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/* CompliantNode refers to a node that follows the rules (not malicious)*/
public class CompliantNode implements Node {


    private Map<Transaction, Set<Integer>> receivedTransactions = new HashMap<>();
    private Map<Transaction, Integer> uniqueTransactionCounts = new HashMap<>();

    private int numNodes = 0;

    private static int MIN_UNIQUE_TRANSACTIONS = 4;


    public CompliantNode(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
        // blank for now
    }

    public void setFollowees(boolean[] followees) {
        this.numNodes = followees.length;
    }

    public void setPendingTransaction(Set<Transaction> pendingTransactions) {

        for (Transaction tx : pendingTransactions) {
            uniqueTransactionCounts.put(tx, 1);
        }
    }

    public Set<Transaction> sendToFollowers() {
        // this simple algorithm will just check which transaction were common among all the received transactions
        int numConfirmNeeded = numNodes < MIN_UNIQUE_TRANSACTIONS ? 1 : MIN_UNIQUE_TRANSACTIONS;
        Set<Transaction> agreedTransactions = new HashSet<>();

        for (Map.Entry<Transaction, Integer> entry : uniqueTransactionCounts.entrySet()) {
            if (entry.getValue() >= numConfirmNeeded) {
                agreedTransactions.add(entry.getKey());
            }
        }

        return agreedTransactions;
    }

    public void receiveFromFollowees(Set<Candidate> candidates) {
        for (Candidate candidate : candidates) {
            if (!receivedTransactions.containsKey(candidate.tx)) {
                receivedTransactions.put(candidate.tx, new HashSet<>());
            }

            if (!receivedTransactions.get(candidate.tx).contains(candidate.sender)) {
                receivedTransactions.get(candidate.tx).add(candidate.sender);
                if (!uniqueTransactionCounts.containsKey(candidate.tx)) {
                    uniqueTransactionCounts.put(candidate.tx, 0);
                }
                uniqueTransactionCounts.put(candidate.tx, uniqueTransactionCounts.get(candidate.tx) + 1);
            }
        }
    }
}
