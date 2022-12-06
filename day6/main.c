// aoc 2022 day 6 in c
// a small relief after parsing that ascii art yesterday

#include <stdio.h>
#include <string.h>

// change if bugs
#define MAX_LINE_CAP 4097

int areAllCharsDifferent(char buff[], int buffLength) {
	for (int i = 0; i < buffLength; i++) {
		for (int j = i + 1; j < buffLength; j++) {
			if (buff[i] == buff[j])
				return 0;
		}
	}

	return 1;
}

void solve(int n, char* lineOrig) {
	char line[MAX_LINE_CAP];
	strcpy(line, lineOrig);
	int lineLength = strlen(line);
    line[lineLength - 1] = '\0';

    size_t charCount = 0;

    printf("n = %d;\n", n);

    for (size_t i = 0; i < sizeof(line) - n; i ++) {
    	if (areAllCharsDifferent(line + i, n)) {
    		charCount = i + n;
    		break;
    	}
    }
    printf("marker: %d\n", charCount);
}

int main(int argc, char* argv[]) {
    FILE* file = fopen("./input.txt", "r");
    if (file == NULL) {
    	perror("Unable to open file");
    	exit(1);
    }
    char line[MAX_LINE_CAP];

    // supports multiple lines
    while (fgets(line, sizeof(line), file)) {
    	solve(4, line);
    	solve(14, line);
    }

    fclose(file);

    return 0;
}