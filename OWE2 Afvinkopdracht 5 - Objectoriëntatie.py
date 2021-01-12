import re


def read_fastafile(fastafile_name):
    """Extract the headers and the DNA-sequences from the file.

    :param fastafile_name: name of the file
    :return headers: list - headers of the DNA-sequences
    :return dna_seqs: list - DNA-sequences
    """
    # Define the variables.
    headers = []
    seqs = []
    seq = ""

    # Loop through the fa-file and extract the headers and sequences.
    with open(fastafile_name, "r") as fastafile_open:
        for line in fastafile_open:
            stripped_line = line.strip()
            if stripped_line.startswith(">"):
                headers.append(stripped_line)
                seqs.append(seq)
                seq = ""
            else:
                seq += stripped_line

        seqs.append(seq)
        seqs.remove("")

    # Return the headers and the sequences.
    return headers, seqs


class DNA:
    # Initialize the attributes of the class.
    def __init__(self, header, sequence):
        self.__header = header
        self.__genename = ""
        self.__sequence = sequence
        self.__transcript = ""
        self.__gcpercentage = 0

    def set_dna(self, sequence):
        """Accepts the sequence and checks if it is DNA or not.

        :param sequence: DNA-sequence or another type of sequence
        """
        # Check if the sequence is DNA or not. If not, print the result
        # to tell the user. If it is DNA, accept the sequence.
        not_dna = re.search(r"[^ATCG]", sequence)
        if not_dna:
            print("This is not DNA.")
            self.__sequence = ""
        else:
            self.__sequence = sequence

    def get_dna(self):
        """Returns the accepted DNA-sequence.

        :return sequence: DNA-sequence
        """
        # Return the sequence.
        return self.__sequence

    def get_genename(self):
        """Returns the name of the gene.

        :return genename: name of the gene
        """
        # Find the name of the gene in the header.
        genename = re.search(r"^(ENSFCAT000000\d\d\d\d\d\.\d)",
                             self.__header)
        self.__genename = genename

        # Return the name of the gene.
        return self.__genename

    def get_length(self):
        """Returns the length of the sequence.

        :return length: length of the sequence
        """
        return len(self.__sequence)

    def get_transcript(self):
        """Returns the RNA-transcript of the DNA-sequence.

        :return transcript: RNA-transcript of the DNA-sequence
        """
        # Replace all the T's to U's.
        transcript = re.sub("T", "U", self.__sequence)
        self.__transcript = transcript

        # Return the RNA-transcript.
        return self.__transcript

    def get_gcpercentage(self):
        """Calculates the GC-percentage of the DNA-sequence.

        :return gcpercentage: percentage of G and C in the sequence
        """
        # If the length of the sequence is 0, there is no sequence and
        # the GC-percentage cannot be calculated. Otherwise, the
        # GC-percentage is calculated and returned.
        if len(self.__sequence) == 0:
            print("There is no sequence.")
        else:
            total_gc = self.__sequence.count("G") + \
                       self.__sequence.count("C")
            gcpercentage = round(total_gc/len(self.__sequence)*100, 2)
            self.__gcpercentage = gcpercentage
            return self.__gcpercentage


if __name__ == '__main__':
    # Define the variables.
    file = "OWE2 Afvinkopdracht 5 - Felis catus.fa"
    dna_sequences = []
    sequences = []
    lengths = []
    transcrips = []
    gc_percentages = []

    # Call the functions.
    headers, seqs = read_fastafile(file)

    # Add each object to a list.
    for i in range(len(seqs)):
        dna_sequences.append(DNA(headers[i], seqs[i]))

    # Add the name and GC-percentage of each object to a list.
    for seq in dna_sequences:
        sequences.append(seq.get_dna())
        lengths.append(seq.get_length())
        transcrips.append(seq.get_transcript())
        gc_percentages.append(seq.get_gcpercentage())

    # Find the index of the highest GC-percentage.
    index = gc_percentages.index(max(gc_percentages))

    # Print the gene name of the highest GC-percentage and
    # the percentage itself.
    print("Header:", headers[index])
    print("DNA-sequence:", sequences[index])
    print("Length:", lengths[index])
    print("RNA-transcript:", transcrips[index])
    print("GC-percentage:", gc_percentages[index])
