#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main() {
    double num1, num2;
    char op;
    char input;
    string out;
    double power,base;
    while (true) {
        cout << "Enter 'c' or 'q' to quit): ";
        cin >> input;
        
        // Check if user wants to quit
        if (input == 'q') {
            cout << "Calculator exited." << endl;
            break;
        }

        cout<<"Enter first number:";
        cin>>num1;
        cout << "Enter an operator (+, -, *, /, ^, r for sqrt, s for sin, c for cos, t for tan, l for log): ";
        cin >> op;
        switch (op) {
            case 'r': cout << "Result: " << sqrt(num1) << endl; break;
            case 's': cout << "Result: " << sin(num1) << endl; break;
            case 'c': cout << "Result: " << cos(num1) << endl; break;
            case 't': cout << "Result: " << tan(num1) << endl; break;
            case 'l': cout << "Result: " << log(num1) << endl; break;
            default: cout << "Invalid operator!" << endl;
            }
            break; 
        }
        cout<<"Do you want to use power func(yes/no): ";
        cin>>out;
        if(out=="yes"){
        	cout<<"Enter base for power: ";
        	cin>>base;
        	cout<<"Enter power: ";
        	cin>>power;
        	cout<<"Result: "<<pow(base,power);
		}
		else{
			cout<<"Moving to next";
		}
		cout << "\nEnter second number: ";
        cin >> num2;
        cout << "Enter an operator (+, -, *, /, ^, r for sqrt, s for sin, c for cos, t for tan, l for log): ";
        cin >> op;
        switch (op) {
            case '+': cout << "Result: " << num1 + num2 << endl; break;
            case '-': cout << "Result: " << num1 - num2 << endl; break;
            case '*': cout << "Result: " << num1 * num2 << endl; break;
            case '/': 
                if (num2 != 0)
                    cout << "Result: " << num1 / num2 << endl;
                else
                    cout << "Error! Division by zero." << endl;
                break;
            case '^': cout << "Result: " << pow(num1, num2) << endl; break;
            default: cout << "Invalid operator!" << endl;
        }
    return 0;
}

