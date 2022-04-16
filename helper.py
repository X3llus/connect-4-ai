from time import sleep
import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores, a1_rew, a2_rew):
    # print(scores, mean_scores)
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Number of turns per game played (lower is better)')
    plt.xlabel('Number of Games')
    plt.ylabel('Total Game Turns')
    plt.subplot(2, 1, 1)
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.legend(['Turns', 'Average Turns'])

    plt.subplot(2, 1, 2)
    plt.plot(a1_rew)
    plt.plot(a2_rew)
    # plt.text(len(scores)-1, a1_rew[-1], str(a1_rew[-1]))
    # plt.text(len(scores)-1, a2_rew[-1], str(a2_rew[-1]))
    plt.legend(['a1 score', 'a2 score'])
    plt.show(block=False)
    plt.pause(0.1)