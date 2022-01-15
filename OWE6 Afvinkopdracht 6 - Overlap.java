public class Main {

    public static final String [] names = {"Rosalind_0498", "Rosalind_2391", "Rosalind_2323", "Rosalind_0442", "Rosalind_5013"};
    public static final String [] seqs = {"AAATAAA", "AAATTTT", "TTTTCCC", "AAATCCC", "GGGTGGG"};


    public static String reverseString(String forward) {
        // Define the variables.
        String reverse = "";
        char character;

        // Loop through the string and reverse it.
        for (int i = 0; i < forward.length(); i++) {
            character = forward.charAt(i);
            reverse = character + reverse;
        }
        // Return the reversed string.
        return reverse;
    }


    public static int determineOverlap(String firstSeq, String secondSeq) {
        // Define the variables.
        boolean cont = true;
        int overlap = 0;

        // Determine the overlap in the strings.
        for (int i = 0; i < firstSeq.length(); i++) {
            secondSeq = reverseString(secondSeq);
            if (firstSeq.charAt(i) == secondSeq.charAt(i)) {
                overlap++;
            } else {
                break;
            }
        }
        // Return the number of characters that overlap.
        return overlap;
    }


    public static void main(String[] args) {
        // Compare the strings.
        for (int i = 0; i < names.length; i++) {
            for (int k = 0; k < names.length; k++) {
                int overlap = determineOverlap(seqs[i], seqs[k]);

                // Print the results in the console if they meet the requirements.
                if (overlap > 0 && overlap < seqs[i].length()) {
                    System.out.println(names[k] + " " + names[i]);
                }
            }
        }
    }
}
