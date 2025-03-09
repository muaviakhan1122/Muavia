#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>

using namespace std;

// Function to convert string to lowercase
string toLowerCase(string str) {
    transform(str.begin(), str.end(), str.begin(), ::tolower);
    return str;
}

// Function to check if a disease matches user symptoms
bool matchSymptoms(vector<string> diseaseSymptoms, vector<string> userSymptoms) {
    int matchCount = 0;

    for (const auto& symptom : userSymptoms) {
        for (const auto& diseaseSymptom : diseaseSymptoms) {
            if (toLowerCase(symptom) == toLowerCase(diseaseSymptom)) {
                matchCount++;
                break;
            }
        }
    }

    return matchCount > 1;  // If at least 2 symptoms match, consider it a possible disease
}

int main() {
    ifstream file("book1.csv");  // Open the CSV file
    if (!file.is_open()) {
        cout << "Error: Could not open the file!" << endl;
        return 1;
    }

    vector<vector<string>> diseases;
    string line, word;

    // Read CSV file and store data
    while (getline(file, line)) {
        vector<string> row;
        stringstream ss(line);

        while (getline(ss, word, ',')) {
            row.push_back(word);
        }
        diseases.push_back(row);
    }

    file.close();

    // Get user symptoms
    cout << "Enter your symptoms (comma-separated): ";
    string userInput;
    getline(cin, userInput);

    // Convert user input into a vector of symptoms
    vector<string> userSymptoms;
    stringstream ss(userInput);
    while (getline(ss, word, ',')) {
        userSymptoms.push_back(toLowerCase(word));  // Convert to lowercase
    }

    // Find possible diseases
    vector<string> matchingDiseases;
    for (const auto& disease : diseases) {
        if (disease.size() > 1 && matchSymptoms({disease.begin() + 1, disease.end()}, userSymptoms)) {
            matchingDiseases.push_back(disease[0]);
        }
    }

    // Display results
    if (matchingDiseases.empty()) {
        cout << "No matching disease found. Please consult a doctor." << endl;
    } else {
        cout << "Possible diseases based on your symptoms:\n";
        for (const auto& disease : matchingDiseases) {
            cout << "- " << disease << endl;
        }
    }

    return 0;
}
