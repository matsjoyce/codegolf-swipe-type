#include<iostream>
#include<fstream>
#include<vector>
#include<map>
#include<algorithm>
#include<utility>
#include<cmath>

using namespace std;

const double RESOLUTION = 3.2;

double dist(const pair<double, double>& a, const pair<double, double>& b) {
    return sqrt((a.first - b.first) * (a.first - b.first) + (a.second - b.second) * (a.second - b.second));
}

double helper(const vector<pair<double, double> >& a,
        const vector<pair<double, double> >& b,
        vector<vector<double> >& dp,
        int i,
        int j) {
    if (dp[i][j] > -1)
        return dp[i][j];
    else if (i == 0 && j == 0)
        dp[i][j] = dist(a[0], b[0]);
    else if (i > 0 && j == 0)
        dp[i][j] = helper(a, b, dp, i - 1, 0) +
                   dist(a[i], b[0]);
    else if (i == 0 && j > 0)
        dp[i][j] = helper(a, b, dp, 0, j - 1) +
                   dist(a[0], b[j]);
    else if (i > 0 && j > 0)
        dp[i][j] = min(min(helper(a, b, dp, i - 1, j),
                           helper(a, b, dp, i - 1, j - 1)),
                       helper(a, b, dp, i, j - 1)) +
                   dist(a[i], b[j]);
    return dp[i][j];
}

double discretefrechet(const vector<pair<double, double> >& a, const vector<pair<double, double> >& b) {
    vector<vector<double> > dp = vector<vector<double> >(a.size(), vector<double>(b.size(), -1.));
    return helper(a, b, dp, a.size() - 1, b.size() - 1);
}

bool issubsequence(string& a, string& b) {
    // Accounts for repetitions of the same character: hallo subsequence of halo
    int i = 0, j = 0;
    while (i != a.size() && j != b.size()) {
        while (a[i] == b[j])
            ++i;
        ++j;
    }
    return (i == a.size());
}

int main() {
    string swipedword;
    cin >> swipedword;

    ifstream fin;
    fin.open("wordlist");
    map<string, double> candidatedistance = map<string, double>();
    string readword;
    while (fin >> readword) {
        if (issubsequence(readword, swipedword) && readword[0] == swipedword[0] && readword[readword.size() - 1] == swipedword[swipedword.size() - 1]) {
            candidatedistance[readword] = -1.;
        }
    }
    fin.close();

    ifstream fin2;
    fin2.open("keypos.csv");
    map<char, pair<double, double> > keypositions = map<char, pair<double, double> >();
    char rc, comma;
    double rx, ry;
    while (fin2 >> rc >> comma >> rx >> comma >> ry) {
        keypositions[rc] = pair<double, double>(rx, ry);
    }
    fin2.close();

    vector<pair<double, double> > swipedpath = vector<pair<double, double> >();
    for (int i = 0; i != swipedword.size(); ++i) {
        swipedpath.push_back(keypositions[swipedword[i]]);
    }

    for (map<string, double>::iterator thispair = candidatedistance.begin(); thispair != candidatedistance.end(); ++thispair) {
        string thisword = thispair->first;
        vector<pair<double, double> > thispath = vector<pair<double, double> >();
        for (int i = 0; i != thisword.size() - 1; ++i) {
            pair<double, double> linestart = keypositions[thisword[i]];
            pair<double, double> lineend = keypositions[thisword[i + 1]];
            double linelength = dist(linestart, lineend);
            if (thispath.empty() || linestart.first != thispath[thispath.size() - 1].first || linestart.second != thispath[thispath.size() - 1].second)
                thispath.push_back(linestart);
            int segmentnumber = linelength / RESOLUTION;
            for (int j = 1; j < segmentnumber; ++j) {
                thispath.push_back(pair<double, double>(linestart.first + (lineend.first - linestart.first) * ((double)j) / ((double)segmentnumber),
                                    linestart.second + (lineend.second - lineend.second) * ((double)j) / ((double)segmentnumber)));
            }
        }
        pair<double, double> lastpoint = keypositions[thisword[thisword.size() - 1]];
        if (thispath.empty() || lastpoint.first != thispath[thispath.size() - 1].first || lastpoint.second != thispath[thispath.size() - 1].second)
        thispath.push_back(lastpoint);

        thispair->second = discretefrechet(thispath, swipedpath) / (double)(thispath.size());
    }

    double bestscore = 1e9;
    string bestword = "";
    for (map<string, double>::iterator thispair = candidatedistance.begin(); thispair != candidatedistance.end(); ++thispair) {
        double score = thispair->second;
        if (score < bestscore) {
            bestscore = score;
            bestword = thispair->first;
        }
        // cout << thispair->first << ": " << score << endl;
    }
    cout << bestword << endl;

    return 0;
}