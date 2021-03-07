
from util.ACECA import ACECA, getInitState
import matplotlib.pyplot as plt


init_state = getInitState(100, d_ini=0.5)

aceca1 = ACECA(232, init_state=init_state,run_num=200,alpha=1)
aceca2 = ACECA(232, init_state=init_state,run_num=200,alpha=0.5)
aceca3 = ACECA(232, init_state=init_state,run_num=200,alpha=0.1)

# switch aceca1 ~ 3 to get sub figure
ca = aceca1
#####################################

modelSpace = []
ca.run(isPrint=False)
modelSpace = ca.getModelRatio()

model = "L"
dp1 = ['']*ca.run_num
alpha = ca.alpha
if model == "B":
    dp1[0] = 1
else:
    dp1[0] = 0

for i in range(1,200):
    dp1[i] = dp1[i-1] * (1-alpha) + alpha / 3
    


model_L = []
for row in modelSpace:
    model_L.append(row["L"])

plt.figure()
plt.plot(range(ca.run_num), model_L, 'o',label = "Experimental L",ms = 3)
plt.plot(range(ca.run_num), dp1, label = "Theoretical L")
plt.xlabel("Time step")
plt.ylabel("Ratio")
plt.ylim([0,1])
plt.title("alpha = "+str(ca.alpha))