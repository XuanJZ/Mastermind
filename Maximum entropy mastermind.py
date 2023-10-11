import copy
import math

colours = ["purple","pink","blue","green","orange"]  #insert however many colours
N = 4


def feedback(code,guess,N):
    done_count = 0
    feedback = []
    for x in range(N):
        if code[x] == guess[x]:
            code[x] = code[x] +"*"
            guess[x]= guess[x] +"^"
            done_count += 1
            feedback.append("red")
    
    for x in range(N):
        for y in range(N):
            if code[x] == guess[y]:
                code[x] = code[x] +"*"
                guess[y]= guess[y] +"^"
                done_count += 1
                feedback.append("white")

    for x in range(N-done_count):
        feedback.append("blank")

    for x in range(N):
        code[x] = code[x].replace('*','')
    for x in range(N):
        guess[x] = guess[x].replace('^','')
    return feedback

def entropy(feedback_dic,size):
    feedbacks = list(feedback_dic.keys())
    ent = 0
    for x in range(len(feedbacks)):
        prob = feedback_dic[feedbacks[x]]/size
        ent += prob*math.log(1/prob,2)
    return ent

def deepcopy(pool):
    another_pool = copy.deepcopy(pool)
    return(pool,another_pool)


def guesser(pool_1,pool_2,last_pool):
    feedback_dic_deep = {}
    max_ent = float('-inf')
    print_once = True
    for guess in pool_1:
        pool_size = 0
        feedback_dic = {}
        for y in pool_2:
            feedback_key = tuple(feedback(guess,y,N))
            if not feedback_key in feedback_dic:
                feedback_dic.update({feedback_key:1})
            elif feedback_key in feedback_dic:
                feedback_dic[feedback_key] += 1
            pool_size += 1
        if entropy(feedback_dic,pool_size) > max_ent:
            feedback_dic_deep = {}
            max_ent = entropy(feedback_dic,pool_size) 
            optimal_guess = copy.deepcopy(guess)
            for a in pool_2:
                feedback_key_deep = tuple(feedback(guess,a,N))
                if not feedback_key_deep in feedback_dic_deep:
                    feedback_dic_deep.update({feedback_key_deep:[a]})
                elif feedback_key_deep in feedback_dic_deep:
                    feedback_dic_deep[feedback_key_deep].append(a)
        if print_once:
            actual_Ent = math.log(last_pool,2)-math.log(pool_size,2)
            print_once = False
    return optimal_guess, feedback_dic_deep, max_ent, actual_Ent,pool_size


code_pool=[]
for a in colours:
    for b in colours:
        for c in colours:
            for d in colours:
                creator = [a,b,c,d]
                code_pool.append(creator)


guess_count = {}
while True:
    for x in code_pool:
        solution_pool=[]
        for a in colours:
            for b in colours:
                for c in colours:
                    for d in colours:
                        creator = [a,b,c,d]
                        solution_pool.append(creator)
        pool_1,pool_2 = deepcopy(solution_pool)
        count = 0
        prev_pool_size = len(colours)**N
        flag = True
        print("Code:",x)
        while flag:
            guess, dic, ent, prev_actual_Ent, prev_pool_size= guesser(pool_1,pool_2,prev_pool_size)[0:5]
            fb = tuple(feedback(x,guess,N))
            count += 1
            if prev_actual_Ent != 0:
                print("Actual info content:", prev_actual_Ent)
            print(count, "Guess:",guess,"Entropy:",ent)
            print("Feedback:",fb)
            if guess == x:
                flag = False
                if not count in guess_count:
                    guess_count.update({count:1})
                    print(guess_count)
                elif count in guess_count:
                    guess_count[count] += 1
                    print(guess_count)
            else:
                new_pool = dic[fb]
                pool_1, pool_2 = deepcopy(new_pool)        
    break
















