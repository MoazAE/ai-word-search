import random
from config import DIRS, MAX_EFFORT, N, NUM_WORDS, POOL


# exception هنحتاج ال   
# عشان احنا في ال فنكشن اللي بعدها باكتراك هنقعد ننادي الفنكشن جوا نفسها كتير فا لما عدد المحاولات يعدي الماكس بتاعنا اللي هو كان 1000 عايزين نطلع من كل الفنكشنز اللي جوا بعض دي على طول
class TooHard(Exception):
    pass


class PuzzleGenerator:
    def __init__(self, size=N, num_words=NUM_WORDS, max_effort=MAX_EFFORT, pool=None):
        self.size = size
        self.num_words = num_words
        self.max_effort = max_effort
        self.pool = pool if pool is not None else POOL

        # دي التلت ستايلات اللي عندنا كل واحدة بتاخد الجريد والسيلز وبتشتغل عليهم 
        self.styles = {
            # overlap 
            # sort كل مكان في السيلز عبارة عن مكان على الجريد الفنكشن بترجع مجموع الاماكن اللي لقيتها مش فاضية وبتحط في الاخر سالب عشان فنشن ال 
            # تعتبرها اختيار افضل
            "overlap": lambda grid, cells: -sum(grid[y * self.size + x] != "." for y, x in cells),
            # بالنسبة لل edge
            #   هنا بتفضل لما تبقى اماكن السيلز بعيدة عن النص بتاع الجريد مثال لو حسبت مجموع السيلز دي
            # (0,0) , (0,1) , (0,2)
            # outcome : 18 and with the outside negative it becomes -18 وزي ما قولت السالب بيخليها افضل لما نستعمل عليها فنكشن السورت
            "edge":    lambda grid, cells: -sum(abs(y - (self.size - 1) / 2) + abs(x - (self.size - 1) / 2) for y, x in cells),
            # هنا حرفيا عشوائية وكل ما كان الرقم اصغر كل ما فنكشن السورت اعتمدته الاول
            "random":  lambda grid, cells: random.random(),
        }
        # هنا حرفيا ديكشنري لكل ستايل جواه ليست فاضية هتتملي بعدين بعدد المحاولات الستايل احتاجها عشان يعمل لعبة لما نستعملهم عشان نعرف اني واحدة اسهل واحسن 
        self.history = {s: [] for s in self.styles}

        # دي زي وكانك عملت كل واحدة لوحدها عادي هي هي
        self.effort = self.backtracks = 0
        self.chosen = []          # NEW: cells of every word placed so far, in order (same order as words)

    # Finds all valid grid positions for a word.
    def placements(self, grid, word):
    # هنا الفنكشن دي بتتاكد من كل الاماكن اللي كل حرف من الكلمة ينفع يتحط فيها لو المكان فيه نفس الحرف او فاضي هيعدي غير كدا هنروح للي بعدها
        out = []
        for r in range(self.size):
            for c in range(self.size):
                for dr, dc in DIRS:
    # السطر اللي تحت ده من الاخر بيعمل ليستاية جواها كل الاماكن اللي الكلمة ينفع تتحط فيها بيجرب كل الاتجاهات وكل عمود في كل صف 
    # CAT مثال على كلمة 
    # cat is 3 letters so index 0 1 2 , cells is a list which will have three tuples of placements for each letter of the word cat 
    #let's say the index row in the loop is 3 and column is 2 and the direction is (1,-1) the loop underneath will make the cells = [(3,2),(4,1),(5,0)]
    #which if you look at the grid is a diagonal from right to left      
                    cells = [(r + dr * i, c + dc * i) for i in range(len(word))]
                    if all(0 <= y < self.size and 0 <= x < self.size and grid[y * self.size + x] in ".%s" % ch
                           for (y, x), ch in zip(cells, word)):
    # all makes sure that every condition is true
    # first zip(cells,word) makes it so that every placement is with it's character in the word like this ((3, 2), 'C'), ((4, 1), 'A'), ((5, 0), 'T') 
    # so the if condition only makes sure that everything is true as in y "row index" is bigger or equal to 0 and smaller than the number of grid which is 8 so maximum index is 7
    # column is same as row and that the cell number since our grid is literally a big string of N*N we calculate the index number using y * N + x we make sure that it's either a . which is empty or the character that we are iterating through and if allat is True we append the cells to out
                        out.append(cells)
        return out

    # Puts a word's letters onto the grid.
    # هنا الفنكشن دي حرفيا بتحط الحروف في مكانها في الجريد
    def place(self, grid, word, cells):
    #  بتاخد كوبي من الجريد وبتحطها في ليست عشان تعدل عليها  
        g = list(grid)
        for (y, x), ch in zip(cells, word):
            g[y * self.size + x] = ch
    # هنا ال ريتيرن بترجع الليستاية كا سترينج تاني بعد ما اتعدل عليها
        return "".join(g)

    # Picks the best or random AI placement style.
    def pick_style(self):
    #هنا هيشوفهم واحد واحد قبل اي حاجة هيشوف لو الستايل في الديكشنري عبارة عن ليستاية فاضية هيجربه عشان مجربهوش قبل كدا
        for s in self.styles:
            if not self.history[s]:
                return s
    #    فيه نسبة انو يجرب ستايل عشوائي لو الرقم العشوائي طلع اقل من 0.2 او نسبة 20% يعني
        if random.random() < 0.2:                      
            return random.choice(list(self.styles))
    #  لو عدا من كل حاجة من دي في العادي بيختار احسن ستايل بانه بيروح لكل واحد ويحسب عدد محاولاته على اشتغل كام مرة واقل رقم هيطلع احسن واحد فا هيختاره
    # example : history = {
    #    "overlap": [100, 200, 300],
    #    "edge": [50, 60, 70],
    #    "random": [400, 500, 600]
    #}     
    # (100 + 200 + 300) / 3 = 200 , (50 + 60 + 70) / 3 = 60 , (400 + 500 + 600) / 3 = 500
    # edge اقل رقم ال
        return min(self.styles, key=lambda s: sum(self.history[s]) / len(self.history[s]))

    # Recursively places all words onto the grid.
    # هنا بقى واحدة واحدة انا هشرحها كاملة من فوق هنا عشان مينفعش ادخل جواها هيبقى شكلها معقد
    # grid -> N*N string of "." , words -> list of randomly selected words , i which is index which is 0 , style -> chosen style
    # uses the same global variables that are outside the function
    # if i == len(words) that means the function recurred till the end with no issues 
    # we get this possible placements for the current grid and the current word inside a variable named options and we shuffle them so it lowers the chance of getting the same puzzle twice
    # and then we sort them using the selected style and yes even if we sort them we still need the shuffle since if two placements have the same value the sort is gonna leave them as their original order
    # again options are like this options = [  [(0, 0), (0, 1), (0, 2)], [(2, 1), (2, 2), (2, 3)], [(4, 3), (4, 4), (4, 5)]  ] so cells in options are a list of tuples 
    # now for every time we try a cell the effort += 1 so we can measure if it's taking too many attempts and it's not worth it and if we go over the max effort we raise the exception toohard which interrupts every function in the recursion and stops them
    # now for the bigger picture now let's say the first word is DOG the second is OWL now we go through every cell in options for DOG now let's say we go through the first one now the result awaits for another call of the function backtrack 
    # but this time it's a new grid which is a copy of the original modified with the placement that we used for DOG and i + 1 so it goes to the next word which is OWL now again we see all the possible options for this word with the new grid which DOG is placed in already
    # now we try the same thing with OWL we go through all of it's possible cells now let's say we go through the first one the same cycle repeats with the next words but if the next word doesn't have a valid placement we go back one cycle now let's say we chose a placement for OWL and then the next cycle was FOX but FOX doesn't have any valid placement 
    # then it returns None for the previous cycle which was OWL now owl's loop tries another placement and i think you get the idea by now now let's say it all worked out and the final word found a valid placement the new word placement is placed in the new copied grid it made and the first condition becomes True which then returns the final grid of all placed words the final grid keeps returning to the previous cycles till it returns to the very first one and returns the final grid
    # now again if the effort exceeds max effort we raise the too hard exception and all of this recursion is interrupted and it doesn't make any problems since every cycle edits it's own copied grid
    # also everytime a cycle returns None to it's previous cycle and it makes it's loop try another placement (cells in options) we add + 1 to the backtracks 
    def backtrack(self, grid, words, i, style):
        if i == len(words):
            return grid
        options = self.placements(grid, words[i])
        random.shuffle(options)
        options.sort(key=lambda cells: self.styles[style](grid, cells))
        for cells in options:
            self.effort += 1
            if self.effort > self.max_effort:
                raise TooHard
            self.chosen.append(cells)                       # NEW: try this placement
            result = self.backtrack(self.place(grid, words[i], cells), words, i + 1, style)
            if result:
                return result
            self.chosen.pop()                               # NEW: it failed, undo it
            self.backtracks += 1
        return None

    # Generates a new complete word search puzzle.
    def generate(self):
        # uses the same global effort , backtracks variables
        while True:
        # using the pick_style function to pick a style
            style = self.pick_style()
        # picking random different words from the pool of words how many is indicated by the NUM_WORDS variable
            words = random.sample(self.pool, self.num_words)
        # long words first = fewer dead ends   
            words.sort(key=len, reverse=True)  
        # zeroing everything every loop
            self.effort = self.backtracks = 0
            self.chosen.clear()                              # NEW
            try:
        # here we try the backtrack function to make the grid of our game
                grid = self.backtrack("." * (self.size * self.size), words, 0, style)
            except TooHard:
        # and if we ever raise the toohard exception we catch it here and append to the list of the of the style key in the dictionary and we continue another round of the loop so in summary we try again
                self.history[style].append(self.max_effort)       # punish the style, then try again
                continue
        # here if we actually succeed and get our final grid with all the valid placements 
            if grid:
        # we append the number of efforts it took to the list of the of the style key in the dictionary so that we can check if this is the most efficient when making another puzzle by it taking fewer attempts on average
                self.history[style].append(self.effort)   
                # here we just take the final grid and if there is an empty position which is indicated by "." we replace it with a random character and if not we leave the original character
                grid = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if ch == "." else ch
                               for ch in grid)
                # NEW: also return where every word was placed {word: cells}
                return words, grid, style, self.effort, self.backtracks, dict(zip(words, self.chosen))

    def format_stats(self):
        return "AI's avg attempts (lower = better):  " + "   ".join(
            "%s %.0f" % (s, sum(v) / len(v)) for s, v in self.history.items() if v)
