# solving Riddler Classic @ https://fivethirtyeight.com/features/can-you-flip-your-way-to-victory/

import matplotlib.pyplot as plt


NR_FLIPS = 100

mem = {}


def opt_win_prob_mem(curr_score, nr_flips_left, p_a=0.5):
    """
    compute the probability of winning if playing optimally in a certain situation;
    the situation is defined by the current score and the number of coin flips left
    :param curr_score: current score
    :param nr_flips_left: nr. of coin flips left
    :param p_a: probability of getting +1 when flipping coin A
    :return: probability of winning if playing optimally
    """
    key = (nr_flips_left,curr_score)
    if key in mem:
        return mem[key]
    else:
        if nr_flips_left == 0:  # base case: no moves left
            prob = 1. if curr_score > 0 else 0.
        else:  # general case
            prob = max(
                (1 - p_a) * opt_win_prob_mem(curr_score - 1, nr_flips_left - 1, p_a) +
                p_a * opt_win_prob_mem(curr_score + 1, nr_flips_left - 1, p_a),
                0.5 * opt_win_prob_mem(curr_score - 2, nr_flips_left - 1, p_a) +
                0.5 * opt_win_prob_mem(curr_score + 2, nr_flips_left - 1, p_a),
            )
        mem[key] = prob
        return prob


NR_STEPS = 100
win_probs_by_p_a = {}
for n in range(NR_STEPS + 1):
    mem = {}
    p_a = n / NR_STEPS
    win_prob = opt_win_prob_mem(0, NR_FLIPS, p_a)
    win_probs_by_p_a[p_a] = win_prob

p_as, win_probs = list(win_probs_by_p_a.keys()), list(win_probs_by_p_a.values())
fair_p_a, fair_win_prob = 0.5, win_probs_by_p_a[0.5]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('p')
ax.set_ylabel('probability')
ax.set_title('Winning probability as a function of p')
plt.plot(p_as, win_probs)
plt.scatter(p_as, win_probs)
ax.annotate('  fair coin (%f, %f)' % (fair_p_a, fair_win_prob), (fair_p_a, fair_win_prob))
plt.show()
