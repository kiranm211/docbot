import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


conn = sqlite3.connect('disease_details.db')
c = conn.cursor()

# c.execute("""CREATE TABLE disease (
#             disease_name text primary key ,
#             overview text,
#             causes text ,
#             risks text ,
#             symptoms txt)""")
# conn.commit()

# c.execute("""INSERT INTO disease VALUES (:disease_name, :overview, :causes,:risks, :symptoms)""",{"disease_name": 'Brain aneurysm',
#        "overview": """A brain aneurysm (AN-yoo-riz-um) is a bulge or ballooning in a blood vessel in the brain. It often looks like a berry hanging on a stem.
#
# A brain aneurysm can leak or rupture, causing bleeding into the brain (hemorrhagic stroke). Most often a ruptured brain aneurysm occurs in the space between the brain and the thin tissues covering the brain. This type of hemorrhagic stroke is called a subarachnoid hemorrhage.
#
# A ruptured aneurysm quickly becomes life-threatening and requires prompt medical treatment.
#
# Most brain aneurysms, however, don't rupture, create health problems or cause symptoms. Such aneurysms are often detected during tests for other conditions.
#
# Treatment for an unruptured brain aneurysm may be appropriate in some cases and may prevent a rupture in the future. Talk with your caregiver to ensure you understand the best options for your specific needs.""",
#        "causes": """"The causes of brain aneurysm are unknown, but a range of factors may increase your risk.
#
# """,
#        "risks": """A number of factors can contribute to weakness in an artery wall and increase the risk of a brain aneurysm or aneurysm rupture. Brain aneurysms are more common in adults than in children and more common in women than in men.
#
# Some of these risk factors develop over time; others are present at birth.
#
# Risk factors that develop over time
# These include:
#
# Older age
# Cigarette smoking
# High blood pressure (hypertension)
# Drug abuse, particularly the use of cocaine
# Heavy alcohol consumption
# Some types of aneurysms may occur after a head injury (dissecting aneurysm) or from certain blood infections (mycotic aneurysm).
#
# Risk factors present at birth
# Selected conditions that date to birth can be associated with an elevated risk of developing a brain aneurysm. These include:
#
# Inherited connective tissue disorders, such as Ehlers-Danlos syndrome, that weaken blood vessels
# Polycystic kidney disease, an inherited disorder that results in fluid-filled sacs in the kidneys and usually increases blood pressure
# Abnormally narrow aorta (coarctation of the aorta), the large blood vessel that delivers oxygen-rich blood from the heart to the body
# Cerebral arteriovenous malformation (brain AVM), an abnormal connection between arteries and veins in the brain that interrupts the normal flow of blood between them
# Family history of brain aneurysm, particularly a first-degree relative, such as a parent, brother, sister, or child""",
#        "symptoms": """A sudden, severe headache is the key symptom of a ruptured aneurysm. This headache is often described as the "worst headache" ever experienced.
#
# Common signs and symptoms of a ruptured aneurysm include:
#
# Sudden, extremely severe headache
# Nausea and vomiting
# Stiff neck
# Blurred or double vision
# Sensitivity to light
# Seizure
# A drooping eyelid
# Loss of consciousness
# Confusion
# 'Leaking' aneurysm
# In some cases, an aneurysm may leak a slight amount of blood. This leaking (sentinel bleed) may cause only a:
#
# Sudden, extremely severe headache
# A more severe rupture often follows leaking.
#
# Unruptured aneurysm
# An unruptured brain aneurysm may produce no symptoms, particularly if it's small. However, a larger unruptured aneurysm may press on brain tissues and nerves, possibly causing:
#
# Pain above and behind one eye
# A dilated pupil
# Change in vision or double vision
# Numbness of one side of the face
# When to see a doctor
# Seek immediate medical attention if you develop a:
#
# Sudden, extremely severe headache
# If you're with someone who complains of a sudden, severe headache or who loses consciousness or has a seizure, call 911 or your local emergency number.
#
# Brain aneurysms develop as a result of thinning artery walls. Aneurysms often form at forks or branches in arteries because those sections of the vessel are weaker.
#
# Although aneurysms can appear anywhere in the brain, they are most common in arteries at the base of the brain."""})
#
# conn.commit()
# c.execute("DELETE from disease_info WHERE Overview='Overview' ")
c.execute("SELECT Symptoms FROM disease_info  ")
conn.commit()
dis = c.fetchall()
# print(dis)
names = ['Brain aneurysm', 'Brain tumor', 'Cancer']
while (True):
    user_input = input()
    if 'my symptoms are' in user_input:
        user_input.replace('my symptoms are','')
        print('in')
        list1 = []
        for i in dis:
            for j in i:
                list1.append(j)

        list1.append(user_input)
        # print(list1)
        bot_response = ''
        cm = CountVectorizer().fit_transform(list1)

        similarity_scores = cosine_similarity(cm[-1], cm)
        similarity_scores_list = similarity_scores.flatten()
        index = index_sort(similarity_scores_list)
        index = index[1:]
        j = 0
        k = 1.0
        for i in range(len(index)):
            while (bot_response == ''):

                if similarity_scores_list[index[i]] > k:
                    bot_response = list1[index[i]]
                    response_flag = 1
                    j += 1
                    if j > 2:
                        list1.remove(user_input)
                        break
                if bot_response == '':
                    k = k - 0.001
                if k < 0.0:
                    break

        symp = list(map(str, bot_response.split('$$')))
        print(range(len(symp)), symp)
        symp.reverse()
        for i in range(len(symp)):
            print(symp[i])
            if i > 5:
                break
        print(str(k * 100) + '% Match')
        l = 1

        c.execute("SELECT Disease_name FROM disease_info  WHERE Symptoms= ? ", (bot_response,))
        conn.commit()
        dis_nm = c.fetchall()
        for i in dis_nm:
            for j in i:
                dise_name = j
        return(dise_name)
    else:

        names.append(user_input)
        cn = CountVectorizer().fit_transform(names)
        similarity_scores_names = cosine_similarity(cn[-1], cn)
        similarity_scores_list = similarity_scores_names.flatten()
        index1 = index_sort(similarity_scores_list)
        index1 = index1[1:]
        max = 0.0
        name = ''
        url = ''
        for i in range(len(index1)):
            if similarity_scores_list[index1[i]] > max:
                name = names[index1[i]]
                max = similarity_scores_list[index1[i]]
        names.remove(user_input)
        terms1 = ['Overview', 'Causes', 'Risk_Factors', 'Symptoms', 'When_to_see_a_doctor', 'Complications']
        terms = ['what', 'causes', 'risks', 'symptoms', 'when to see a doctor', 'complications']
        terms.append(user_input)
        cn = CountVectorizer().fit_transform(terms)
        similarity_scores_names = cosine_similarity(cn[-1], cn)
        similarity_scores_list = similarity_scores_names.flatten()
        index1 = index_sort(similarity_scores_list)
        index1 = index1[1:]
        max = 0.0
        term = 'Overview'
        url = ''

        for i in range(len(index1)):
            if similarity_scores_list[index1[i]] > max:
                term = terms[index1[i]]
                max = similarity_scores_list[index1[i]]
        # print(name,terms1[terms.index(term)])
        if term != 'Overview':
            term = terms1[terms.index(term)]
        terms.remove(user_input)

        s = "SELECT " + str(term) + " FROM disease_info  where Disease_name='" + str(name) + "'"
        c.execute(s)
        res1 = ''
        for i in c.fetchall():
            for j in i:
                res1 = res1 + str(j)
                # print(res1)
        res = list(map(str, res1.split('$$')))
        # print(res)
        # l=1
        # try:
        #     for k in range(len(res) - l):
        #         if res[k + 1] == '':
        #             # print(symp[i])
        #             del res[k]
        # except:
        #     l = l + 1
        res = list(filter(('').__ne__, res))
        final = ''
        for i in range(len(res)):
            if 'Open pop-up dialog box Close' in res[i]:
                continue
            else:
                final = final + str(res[i])
        return(final)
        conn.commit()


# c.execute("""UPDATE disease SET symptoms= ? WHERE disease_name=?""",(str(symp),dise_name,))
# conn.commit()
