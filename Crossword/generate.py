import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            words = self.domains[var].copy()
            for word in self.domains[var]:
                if (len(word) != var.length):
                    words.remove(word)
            self.domains[var] = words.copy()


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if not self.crossword.overlaps[x, y]:
            return False
        revision = False
        (i, j) = self.crossword.overlaps[x, y]
        y_letters = set(a[j] for a in self.domains[y])
        words = self.domains[x].copy()
        for word in self.domains[x]:
            if word[i] not in y_letters:
                words.remove(word)
                revision = True
        self.domains[x] = words.copy()
        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = []
            for variable in self.crossword.variables:
                neighbors = self.crossword.neighbors(variable)
                for neighbor in neighbors:
                    arcs.append((variable, neighbor))
        while(len(arcs) != 0):
            arc = arcs[0]
            arcs.remove((arc[0], arc[1]))
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                changed_variables = self.crossword.neighbors(arc[0])
                for x in changed_variables:
                    arcs.append((arc[0], x))
                    arcs.append((x, arc[0]))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        variables = set(x for x in self.domains)
        assigned_variables = set(x for x in assignment)
        if variables == assigned_variables:
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = {y : 0 for x,y in assignment.items()}
        for variable, word in assignment.items():
            words[word] += 1
            if variable.length != len(word):
                return False
            neighbors = self.crossword.neighbors(variable)
            for neighbor in neighbors:
                (i, j) = self.crossword.overlaps[variable, neighbor]
                if variable.cells[i] != neighbor.cells[j]:
                    return False
        for word, count in words.items():
            if count > 1:
                return False
        return True        
        
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        dic = {x : 0 for x in self.domains[var]}
        unassigned_neighbors = set(x for x in self.crossword.neighbors(var) if x not in assignment)
        for word in dic:
            count = 0
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps(var, neighbor)
                for neighbor_word in self.domains[neighbor]:
                    if word[overlap[0]] != neighbor_word[overlap[1]]:
                        count += 1
            dic[word] = count
        dic = [(x,dic[x]) for x in dic]
        dic.sort(key=lambda tupl:tuple[1])
        dic = [x[0] for x in dic]
        return dic
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = set(x for x in self.domains)
        assigned_variables = set(x for x in assignment)
        unassigned_variables = variables - assigned_variables
        min_val = 99999
        min_var = None
        for variable in unassigned_variables:
            val = len(self.domains[variable])
            if val < min_val:
                min_val = val
                min_var = variable
        return min_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment.remove(var)
        return None
                



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
