import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader, None)
        evidence = []
        labels = []
        for row in reader:
            temp = row[:-1]
            temp[0] = int(temp[0])
            temp[1] = float(temp[1])
            temp[2] = int(temp[2])
            temp[3] = float(temp[3])
            temp[4] = int(temp[4])
            temp[5] = float(temp[5])
            temp[6] = float(temp[6])
            temp[7] = float(temp[7])
            temp[8] = float(temp[8])
            temp[9] = float(temp[9])
            temp[10] = 0 if temp[10] == 'Jan' else 1 if temp[10] == 'Feb' else 2 if temp[10] == 'Mar' else 3 if temp[10] == 'Apr' else 4 if temp[10] == 'May' else 5 if temp[10] == 'Jun' else 6 if temp[10] == 'Jul' else 7 if temp[10] == 'Aug' else 8 if temp[10] == 'Sep' else 9 if temp[10] == 'Oct' else 10 if temp[10] == 'Nov' else 11
            temp[11] = int(temp[11])
            temp[12] = int(temp[12])
            temp[13] = int(temp[13])
            temp[14] = int(temp[14])
            temp[15] = 1 if temp[15] == 'Returning_Visitor' else 0
            temp[16] = 0 if temp[16] == 'FALSE' else 1
            evidence.append(temp)
            labels.append(0 if row[-1] == 'FALSE' else 1)
        return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(evidence, labels)
    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    total_positive = 0
    total_negative = 0
    identified_positive = 0
    identeified_negative = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            total_positive += 1
            if predictions[i] == 1:
                identified_positive += 1
        if labels[i] == 0:
            total_negative +=1
            if predictions[i] == 0:
                identeified_negative += 1
    sensitivity = identified_positive / total_positive
    specificity = identeified_negative / total_negative
    return (sensitivity, specificity)
    


if __name__ == "__main__":
    main()
