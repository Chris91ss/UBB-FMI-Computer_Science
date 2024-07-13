#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

// int main() {
//     vector<string> v{ "rain", "in", "spain", "falls", "mainly", "plain" };
//     sort(v.begin(), v.end(), [](string a, string b) { return a > b; });
//     // "spain", "rain", "plain", "mainly", "in", "falls"
//     vector<string>::iterator it = v.begin() + 4;
//     *it = "brain";
//     //"spain", "rain", "plain", "mainly", "brain", "falls"
//     it = v.begin();
//     while (it != v.end()) {
//         string aux = *it;
//         char c1 = aux[aux.size() - 3];
//         char c2 = aux[aux.size() - 2];
//         char c3 = aux[aux.size() - 1];
//         if (c1 == 'a' && c2 == 'i' && c3 == 'n')
//             cout << *it << "\n";
//         it++;
//     }
//     return 0;
// }

// spain rain plain brain
