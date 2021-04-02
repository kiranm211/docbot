import warnings
import sqlite3
import nltk
from flask import Flask, render_template, request, Blueprint
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import random
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from flask import Blueprint, render_template, request
import os
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

gsearch = Blueprint("gsearch", __name__, static_folder="static", template_folder="templates/search")
warnings.filterwarnings('ignore')




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


class driver:
    symp = []
    flag = 0
    docname = ''
    diseasename = ''
    i = 0
    username = ''
    filechecker = 0
    filename = ''
    j = 0
    k = 0
    s = 0
    date =''
    time =''


def create_file(name1):
    file = open(name1, 'w')
    file.close()


def write_to_file(name1, data):
    with open(name1, 'a') as f:
        f.write(data + "\n")


# random greeting
def bot_response(user_input, static=None):
    global response_flag
    response = ''


    if user_input.lower() == 'yes':
        if driver.flag==2 and driver.i==7 and driver.s<=5:
            pass
        else:
            driver.flag += 1

        try:
            print('try',driver.diseasename)
            if driver.flag == 1:
                query ='doctor who can treat '+ driver.diseasename + ' near me'
                # print(query)
                url = ''
                for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                    url = j
                print(url)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'lxml')
                match = soup.find_all('div', class_="info-section")
                # match
                link = soup.find_all(['a', 'h3'], limit=15)
                j = 0

                for links in link:
                    if j < 7:
                        if links.text == '11000+ Teleconsultations Successfully Assisted Across India. Book Now! ':
                            pass
                        if links.text != 'You do not have permission to view this directory or page using the credentials that you supplied.':
                            response = response + ' ' + links.text
                    else:
                        break
                    j += 1
                driver.docname = link[1].text
                if response == '':
                    pass
                return response


        except :
            print('execpt', driver.diseasename)
            response = ''
            if driver.flag == 1:
                query = 'doctor near me '
                # print(query)
                url = ''
                for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                    url = j
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'lxml')
                match = soup.find_all('div', class_="info-section")
                # match
                link = soup.find_all(['a', 'h3'], limit=15)
                j = 0
                print(link)
                for links in link:
                    if j < 7:
                        if links.text != 'You do not have permission to view this directory or page using the credentials that you supplied.':
                            response = response + ' ' + links.text
                    else:
                        break
                    j += 1
                driver.docname = link[1].text
                return response
    names = ['22q11.2 deletion syndrome', 'A fib', 'Abdominal aortic aneurysm', 'Abnormally excessive sweating',
             "Abscess Bartholin's", 'Absence seizure', 'AC joint separation', 'Acanthosis nigricans', 'Achalasia',
             'Achilles ten dinitis', 'Achilles tendon rupture', 'Acid reflux', 'Acid reflux infant', 'ACL injury',
             'Acne', 'Acoustic neuroma', 'Acquired immunodeficiency syndrome', 'Acromegaly',
             'Acromioclavicular joint separation', 'Actinic keratosis', 'Acute coronary syndrome',
             'Acute febrile neutrophilic dermatosis', 'Acute flaccid myelitis (AFM)',
             'Acute inflammatory demyelinating polyneuropathy', 'Acute kidney failure', 'Acute liver failure',
             'Acute lymphoblastic leukemia', 'Acute lymphocytic leukemia', 'Acute lymphoid leukemia',
             'Acute myelogenous leukemia', 'Acute radiation sickness', 'Acute radiation syndrome',
             'Acute renal failure', 'Acute respiratory distress syndrome', 'Acute sinusitis', 'Addiction alcohol',
             'Addiction drug', 'Addiction gambling', 'Addiction nicotine', "Addison's disease",
             'Adenitis mesenteric',
             'Adenomyosis', 'ADHD in children', 'ADHD Adult', 'Adhesive capsulitis', 'Adjustment disorders',
             'Adnexal tumors', 'Adolescent schizophrenia', 'Adrenal cancer', 'Adrenal gland tumor', 'Adrenal mass',
             'Adrenoleukodystrophy', 'Adult attention-deficit/hyperactivity disorder (ADHD)',
             "Adult Still's disease",
             'AFM', 'Age spots (liver spots)', 'Age-related macular degeneration dry',
             'Age-related macular degeneration wet', 'Agnogenic myeloid metaplasia', 'Agoraphobia', 'AIDP',
             'AIDS/HIV',
             'Airplane ear', 'Albinism', 'Alcohol addiction', 'Alcohol intolerance', 'Alcohol poisoning',
             'Alcohol use disorder', 'Alcoholic hepatitis', 'Aldosteronoma', 'Allergic granulomatosis',
             'Allergic granulomatosis and angiitis', 'Allergic rhinitis', 'Allergies', 'Allergy dust mite',
             'Allergy egg', 'Allergy food', 'Allergy latex', 'Allergy milk', 'Allergy mold', 'Allergy nickel',
             'Allergy peanut', 'Allergy penicillin', 'Allergy pet', 'Allergy shellfish', 'Allergy soy',
             'Allergy wheat',
             'Alopecia', 'Alpha-gal syndrome', 'ALS', 'Alveolar osteitis', "Alzheimer's disease",
             'Ambiguous genitalia',
             'Amblyopia', 'Ameloblastoma', 'Amenorrhea', 'American trypanosomiasis', 'Amnesia',
             'Amnesia dissociative',
             'Amnesia transient global', 'Amnestic syndrome', 'Amniotic fluid embolism', 'Ampullary cancer',
             'Amyloidosis', 'Amyotrophic lateral sclerosis (ALS)', 'Anal cancer', 'Anal fissure', 'Anal fistula',
             'Anal itching', 'Anaphylaxis', 'Anaplasmosis', 'Anemia', 'Anemia aplastic', "Anemia Cooley's",
             'Anemia iron deficiency', 'Anemia Mediterranean', 'Anemia sickle cell', 'Anemia vitamin deficiency',
             'Aneurysm abdominal aortic', 'Aneurysm aortic', 'Aneurysm brain', 'Aneurysm cerebral',
             'Aneurysm popliteal', 'Aneurysm thoracic aortic', 'Aneurysms', 'Angelman syndrome', 'Angiitis',
             'Angina',
             'Angina pectoris', 'Angioedema and hives', 'Angiofollicular lymph node hyperplasia', 'Angiosarcoma',
             'Anhidrosis', 'Ankle fracture', 'Ankle sprain', 'Ankyloglossia', 'Ankylosing spondylitis', 'Anorexia',
             'Anorexia nervosa', 'Anorgasmia in women', 'Anterior cruciate ligament injury',
             'Anterior prolapse (cystocele)', 'Anthrax', 'Antibiotic-associated colitis',
             'Antibiotic-associated diarrhea', 'Antiphospholipid syndrome', 'Antisocial personality disorder',
             'Anxiety disorder generalized', 'Anxiety disorder social', 'Anxiety disorders', 'Aortic aneurysm',
             'Aortic coarctation', 'Aortic dissection', 'Aortic valve disease', 'Aortic valve regurgitation',
             'Aortic valve stenosis', 'Aphasia', 'Aphasia primary progressive', 'Aphthous ulcer',
             'Apical ballooning syndrome', 'Aplastic anemia', 'Appendicitis', 'ARDS', 'Arenaviruses',
             'Argentine hemorrhagic fever', 'Arm fracture', 'Arrhythmia', 'Arteriosclerosis / atherosclerosis',
             'Arteriovenous fistula', 'Arteriovenous malformation', 'Arteritis giant cell', "Arteritis Takayasu's",
             'Arthritis', 'Arthritis basal joint', 'Arthritis degenerative', 'Arthritis gouty',
             'Arthritis infectious',
             'Arthritis juvenile idiopathic', 'Arthritis osteoarthritis', 'Arthritis psoriatic',
             'Arthritis reactive',
             'Arthritis rheumatoid', 'Arthritis septic', 'Arthritis thumb', 'Asbestosis', 'Ascariasis', 'ASD',
             'Aseptic necrosis', 'Aspergillosis', 'Asthma', 'Asthma attack', 'Asthma childhood',
             'Asthma exercise-induced', 'Asthma occupational', 'Astigmatism', 'Astrocytoma', 'AT', 'Ataxia',
             'Atelectasis', 'Atherosclerosis', "Athlete's foot", 'Atopic dermatitis (eczema)',
             'Atrial fibrillation',
             'Atrial flutter', 'Atrial septal defect (ASD)', 'Atrial tachycardia', 'Atrioventricular canal defect',
             'Atrioventricular nodal reentry tachycardia (AVNRT)', 'Atrioventricular septal defect',
             'Atrophic vaginitis', 'Attachment disorder',
             'Attention-deficit/hyperactivity disorder (ADHD) in children',
             'Attention-deficit/hyperactivity disorder in adults', 'Atypical depression',
             'Atypical hyperplasia of the breast', 'Autism spectrum disorder', 'Autoimmune hepatitis',
             'Autoimmune pancreatitis', 'Autonomic neuropathy', 'Avascular necrosis', 'Avian influenza', 'AVNRT',
             'Baby acne', 'Back pain', 'Bacterial vaginosis', 'Bad breath', 'Bags under eyes', "Baker's cyst",
             'Balance problems', 'Baldness', "Barber's itch", "Barlow's syndrome", 'Barotitis media', 'Barotrauma',
             "Barrett's esophagus", "Bartholin's cyst", 'Basal cell carcinoma', 'Basal joint arthritis', 'BDD',
             'Bedbugs', 'Bedsores (pressure ulcers)', 'Bed-wetting', 'Bee sting', "Behcet's disease",
             "Bell's palsy",
             'Benign adrenal tumors', 'Benign migratory glossitis', 'Benign paroxysmal positional vertigo',
             'Benign paroxysmal positional vertigo (BPPV)', 'Benign peripheral nerve tumor',
             'Benign prostatic hyperplasia (BPH)', "Berger's disease", 'Bicuspid aortic valve', 'Bile duct cancer',
             'Bile reflux', 'Binge drinking', 'Binge-eating disorder', 'Bipolar disorder',
             'Bird flu (avian influenza)',
             'Black hairy tongue', 'Blackheads', 'Bladder calculi', 'Bladder cancer', 'Bladder control loss of',
             'Bladder exstrophy', 'Bladder infection', 'Bladder inflammation', 'Bladder prolapse', 'Bladder stones',
             'Blastocystis hominis', 'Blepharitis', 'Blocked tear duct', 'Blood in urine (hematuria)',
             'Blood pressure high', 'Blood pressure low', 'BMS', 'Body dysmorphic disorder', 'Body lice',
             'Body odor and sweating', 'Boils and carbuncles', 'Bone cancer', 'Bone infection', 'Bone metastasis',
             'Bone spurs', 'Borderline personality disorder', 'Botulism', 'Bowel incontinence', 'Bowel obstruction',
             'BPH', 'Brachial plexus injury', 'Bradycardia', 'Bradycardia-tachycardia syndrome', 'Brain aneurysm',
             'Brain arteriovenous malformation', 'Brain attack', 'Brain AVM (arteriovenous malformation)',
             'Brain metastases', 'Brain tumor', 'Brain tumor child', 'Breast cancer', 'Breast cancer inflammatory',
             'Breast cancer male', 'Breast cysts', 'Breast infection', 'Breast pain', 'Broken ankle', 'Broken arm',
             'Broken blood vessel in eye', 'Broken collarbone', 'Broken foot', 'Broken hand',
             'Broken heart syndrome',
             'Broken hip', 'Broken leg', 'Broken nose', 'Broken ribs', 'Broken toe', 'Broken wrist',
             'Bronchiolitis',
             'Bronchitis', 'Brucellosis', 'Brugada syndrome', 'Bruxism (teeth grinding)', "Buerger's disease",
             'Bulimia nervosa', 'Bullous pemphigoid', 'Bundle branch block', 'Bunions', 'Bunyaviruses',
             'Burn injury',
             'Burning mouth syndrome', 'Burning thigh pain', 'Burns', 'Bursitis', 'Bursitis of the knee',
             'C. difficile colitis', 'C. difficile infection', 'Calciphylaxis', 'Calluses and corns', 'Cancer',
             'Cancer acute lymphocytic leukemia', 'Cancer acute myelogenous leukemia', 'Cancer anal',
             'Cancer basal cell', 'Cancer bladder', 'Cancer bone', 'Cancer breast', 'Cancer carcinoid tumors',
             'Cancer cervical', 'Cancer chronic lymphocytic leukemia', 'Cancer chronic myelogenous leukemia',
             'Cancer colon', 'Cancer endometrial', 'Cancer esophageal', 'Cancer eye melanoma', 'Cancer gallbladder',
             'Cancer gastric', 'Cancer hairy cell leukemia', "Cancer Hodgkin's disease", 'Cancer Hurthle cell',
             'Cancer inflammatory breast', 'Cancer kidney', 'Cancer leukemia', 'Cancer lip', 'Cancer liver',
             'Cancer lung', 'Cancer male breast', 'Cancer Merkel cell', 'Cancer mesothelioma', 'Cancer mouth',
             'Cancer multiple myeloma', 'Cancer nasopharyngeal', 'Cancer neuroblastoma',
             "Cancer non-Hodgkin's lymphoma", 'Cancer oral', 'Cancer ovarian', 'Cancer pancreatic',
             'Cancer paraneoplastic syndromes', 'Cancer prostate', 'Cancer rectal', 'Cancer retinoblastoma',
             'Cancer skin', 'Cancer soft tissue sarcoma', 'Cancer squamous cell', 'Cancer stomach',
             'Cancer testicular',
             'Cancer throat', 'Cancer thyroid', 'Cancer uterine', 'Cancer vagina', 'Cancer vulvar',
             "Cancer Wilms' tumor", 'Candidiasis oral', 'Candidiasis vaginal', 'Cankersore',
             'Carbon monoxide poisoning', 'Carbuncles and boils', 'Carcinoid syndrome', 'Carcinoid tumors',
             'Carcinoma of unknown primary', 'Cardiac arrest sudden', 'Cardiac ischemia', 'Cardiogenic shock',
             'Cardiomegaly', 'Cardiomyopathy', 'Cardiomyopathy dilated', 'Cardiomyopathy hypertrophic',
             'Cardiovascular disease', 'Carotid artery disease', 'Carpal tunnel syndrome', 'Castleman disease',
             'Cataracts', 'Cavernous malformations', 'Cavities/tooth decay', 'Celiac disease', 'Cellulite',
             'Cellulitis', 'Central nervous system vascular malformations', 'Central sleep apnea',
             'Cercarial dermatitis', 'Cerebral aneurysm', 'Cerebral palsy', 'Cerumen impaction', 'Cervical cancer',
             'Cervical dystonia', 'Cervical osteoarthritis', 'Cervical spondylosis', 'Cervicitis', 'Chagas disease',
             'Charcot-Marie-Tooth disease', 'CHD', 'Chemical dependency', 'Chemo brain', 'Chest pain',
             'Chest wall pain', 'Chiari malformation', 'Chickenpox', 'Chilblains', 'Child abuse',
             'Child maltreatment',
             'Childhood apraxia of speech', 'Childhood asthma', 'Childhood obesity', 'Childhood schizophrenia',
             'Chlamydia trachomatis', 'Cholangiocarcinoma (bile duct cancer)', 'Cholangitis primary sclerosing',
             'Cholecystitis', 'Cholera', 'Cholestasis of pregnancy', 'Cholesterol high blood', 'Chondrosarcoma',
             'Chordoma', "Chorea Huntington's", 'Choroid plexus carcinoma', 'Chronic adrenal insufficiency',
             'Chronic cough', 'Chronic daily headaches', 'Chronic exertional compartment syndrome',
             'Chronic fatigue syndrome', 'Chronic granulomatous disease', 'Chronic hives', 'Chronic kidney disease',
             'Chronic kidney failure', 'Chronic lymphocytic leukemia', 'Chronic lymphocytic thyroiditis',
             'Chronic myelogenous leukemia', 'Chronic obstructive pulmonary disease',
             'Chronic pelvic pain in women',
             'Chronic renal failure', 'Chronic sinusitis', 'Chronic traumatic encephalopathy',
             'Chronic vulvar pain',
             'Churg-Strauss syndrome', 'Cirrhosis', 'CJD', 'CKD', 'Claudication', 'Cleft lip and cleft palate',
             'Click-murmur syndrome', 'Clinical depression', 'CLL', 'Clostridioides difficile infection',
             'Clostridium difficile infection', 'Clubfoot', 'Cluster headache', 'Coarctation of the aorta',
             'Coccidioidomycosis', 'Cold allergy', 'Cold exposure', 'Cold sore', 'Cold urticaria', 'Cold common',
             'Colic', 'Colitis ischemic', 'Colitis microscopic', 'Colitis pseudomembranous', 'Colitis ulcerative',
             'Collapsed lung', 'Colon cancer', 'Colon polyps', 'Colonic ischemia', 'Colorblindness',
             'Colorectal cancer', 'Coma', 'Common cold', 'Common cold in babies',
             'Common variable immunodeficiency',
             'Common variable immunodeficiency ', 'Common warts', 'Compartment syndrome chronic exertional',
             'Complex regional pain syndrome', 'Complicated bereavement', 'Complicated grief',
             'Compulsive gambling',
             'Compulsive hoarding syndrome', 'Compulsive overeating', 'Compulsive sexual behavior',
             'Compulsive stealing', 'Concussion', 'Condylomata acuminata', 'Congenital adrenal hyperplasia',
             'Congenital heart defects in children', 'Congenital heart disease in adults',
             'Congenital hip dislocation',
             'Congenital megacolon', 'Congenital mitral valve anomalies', 'Congenital myasthenic syndromes',
             'Congenital myopathies', 'Congestive heart failure', 'Conjoined twins', 'Conjunctivitis',
             "Conn's syndrome", 'Constipation', 'Constipation in children', 'Contact dermatitis',
             'Convergence insufficiency', "Cooley's anemia", 'COPD', 'Corns and calluses', 'Corona virus',
             'Coronary artery disease', 'Coronary microvascular disease', 'Coronavirus disease 2019 (COVID-19)',
             'Corticobasal degeneration', 'Costochondritis', 'Costosternal chondrodynia', 'Costosternal syndrome',
             'Cough headaches', 'Cough chronic', 'COVID-19',
             'COVID-19-associated multisystem inflammatory syndrome in children', 'Crabs', 'Cradle cap',
             'Cramp muscle',
             'Cramps menstrual', 'Cranial arteritis', 'Craniopharyngioma', 'Craniosynostosis',
             'Creutzfeldt-Jakob disease', 'Crib death', "Crohn's disease", 'Croup', 'CRPS', 'Cryoglobulinemia',
             'Cryptorchidism', 'Cryptosporidiosis', 'Cryptosporidium infection', 'CTCL', 'Curvature of the penis',
             'Curvature of the spine', 'Cushing syndrome', 'Cutaneous B-cell lymphoma', 'Cutaneous T-cell lymphoma',
             'Cutting/self-injury', 'Cyclic vomiting syndrome', 'Cyclospora infection',
             'Cyclothymia (cyclothymic disorder)', 'Cyclothymic disorder', "Cyst Bartholin's", 'Cyst ganglion',
             'Cyst kidney', 'Cyst ovarian', 'Cyst pancreatic', 'Cyst pilonidal', 'Cyst spermatic',
             'Cystic fibrosis',
             'Cystitis', 'Cystitis interstitial', 'Cysts epidermoid', 'Cysts sebaceous',
             'Cytomegalovirus (CMV) infection', 'Cytomegalovirus infection', 'Dandruff', 'Daytime sleepiness',
             'DCIS',
             'DDH', "De Quervain's tenosynovitis", 'Decreased tear production', 'Deep vein thrombosis (DVT)',
             'Deer-fly fever', 'Deficient color vision', 'Degenerative arthritis', 'Dehydration',
             'Delayed ejaculation',
             'Delayed gastric emptying', 'Delayed sleep phase', 'Delirium', 'Dementia',
             "Dementia Alzheimer's disease",
             'Dementia frontotemporal', 'Dementia Lewy body', 'Dementia vascular', 'Dengue fever',
             'Dengue hemorrhagic fever', 'Dependence nicotine', 'Dependent personality disorder',
             'Depersonalization disorder', 'Depersonalization-derealization disorder',
             'Depression (major depressive disorder)', 'Depression in teenagers', 'Depression postpartum',
             'Dermatitis',
             'Dermatitis atopic', 'Dermatitis cercarial', 'Dermatitis contact', 'Dermatitis scratch',
             'Dermatitis seborrheic', 'Dermatofibrosarcoma protuberans', 'Dermatographia', 'Dermatomyositis',
             'Dermatophytosis', 'Desmoid tumors', 'Desmoplastic small round cell tumors', 'Detached retina',
             'Developmental dysplasia of the hip', 'Deviated septum', "Devic's disease", 'DFSP', 'Diabetes',
             'Diabetes insipidus', 'Diabetes mellitus', 'Diabetes gestational', 'Diabetes type 1',
             'Diabetes type 1 in children', 'Diabetes type 2', 'Diabetes type 2 in children', 'Diabetic coma',
             'Diabetic hyperosmolar syndrome', 'Diabetic hypoglycemia', 'Diabetic ketoacidosis',
             'Diabetic nephropathy',
             'Diabetic neuropathy', 'Diabetic retinopathy', 'Diaper rash', 'Diarrhea',
             'Diarrhea antibiotic-associated',
             "Diarrheatraveler's", 'Difficulty focusing eyes', 'Difficulty speaking', 'Difficulty swallowing',
             'Diffuse idiopathic skeletal hyperostosis (DISH)', 'DiGeorge syndrome (22q11.2 deletion syndrome)',
             'Dilated cardiomyopathy', 'Diphtheria', 'DISH', 'Dislocated elbow', 'Dislocated shoulder',
             'Dislocation',
             'Dissecting aneurysm', 'Dissociative disorders', 'Diverticulitis', 'Dizziness', 'Double uterus',
             'Double-outlet right ventricle', 'Down syndrome', "Dressler's syndrome", 'Drop foot',
             'Drug addiction (substance use disorder)', 'Drug allergy', 'Dry eyes', 'Dry macular degeneration',
             'Dry mouth', 'Dry skin', 'Dry socket', 'DSPS', 'DSRCT', 'Ductal carcinoma in situ (DCIS)',
             'Dumping syndrome', "Dupuytren's contracture", 'Dural arteriovenous fistulas', 'Dust mite allergy',
             'DVT',
             'Dwarfism', 'Dysarthria', 'Dyshidrosis', 'Dyslexia', 'Dysmenorrhea', 'Dyspareunia', 'Dyspepsia',
             'Dysphagia', 'Dysphonia', 'Dysrhythmias', 'Dysthymia', 'Dystonia', 'Dystonia cervical', 'E. coli',
             'Ear infection (middle ear)', 'Ear infection outer ear', 'Eardrum ruptured', 'Early puberty',
             'Earwax blockage', 'Eating disorders', 'Eating disorders anorexia', 'Eating disorders binge eating',
             'Eating disorders bulimia', 'Ebola virus', 'Ebola virus and Marburg virus', 'Ebstein anomaly',
             'Ectopic heartbeat', 'Ectopic pregnancy', 'Ectropion', 'Eczema', 'Eczema dyshidrotic', 'ED', 'Edema',
             'Edema pulmonary', 'Egg allergy', 'Ehlers-Danlos syndrome', 'Ehrlichiosis', 'Eisenmenger syndrome',
             'Elevated blood pressure', 'Embolism pulmonary', 'Embryonal tumors', 'Emphysema', 'Encephalitis',
             'Encopresis', 'End stage renal disease', 'Endocardial cushion defect', 'Endocarditis',
             'Endometrial cancer', 'Endometrial polyps', 'Endometriosis', 'End-stage renal disease',
             'Enlarged breasts in men', 'Enlarged breasts in men (gynecomastia)', 'Enlarged heart',
             'Enlarged liver',
             'Enlarged prostate', 'Enlarged spleen (splenomegaly)', 'Enlarged thyroid', 'Entropion',
             'Eosinophilic esophagitis', 'Eosinophilic granulomatosis with polyangiitis ', 'Ependymoma',
             'Epicondylitis lateral', 'Epidermoid cysts', 'Epidermolysisbullosa', 'Epididymitis',
             'Epidural hematoma',
             'Epiglottitis', 'Epilepsy', 'Epilepsy frontal lobe', 'Epithelioid sarcoma', 'Erectile dysfunction',
             'Erythema infectiosum', 'Erythema multiforme major', 'Escherichia coli infection', 'Esophageal cancer',
             'Esophageal spasms', 'Esophageal varices', 'Esophagitis', 'Essential thrombocythemia',
             'Essential tremor',
             'Esthesioneuroblastoma', 'Ewing sarcoma', 'Excess facial hair in women', 'Excess growth hormone',
             'Excessive daytime sleepiness', 'Excessive menstrual bleeding', 'Exercise headaches',
             'Exercise-induced asthma', 'External compression headaches', 'External otitis', 'Extrasystole',
             'Eye floaters', 'Eye focusing', 'Eye melanoma', 'Eyelid inflammation', 'Eyestrain',
             'Facial hair excess in women', 'Facial palsy', 'Factitious disorder', 'Factor V Leiden',
             'Fallen arches',
             'Fallot tetralogy of', 'Familial adenomatous polyposis', 'Familial hypercholesterolemia',
             'Familial Mediterranean fever', 'Familial paroxysmal peritonitis', 'FAP', 'Farsightedness',
             'Febrile seizure', 'Fecal incontinence', 'Female infertility', 'Female sexual dysfunction',
             'Femoroacetabular impingement', 'Fetal alcohol syndrome', 'Fetal macrosomia', 'Fever', 'Fever blister',
             'Fever valley', 'Fevers viral hemorrhagic', 'FH', 'Fibroadenoma', 'Fibrocystic breasts',
             'Fibroids uterine', 'Fibromuscular dysplasia', 'Fibromyalgia', 'Fibrosis cystic',
             'Fibrosis interstitial pulmonary', 'Fibrosis pulmonary', 'Fibrous dysplasia', 'Fifth disease',
             'Filoviruses', 'Flatfeet', 'Flaviviruses', 'Floaters', 'Floor of the mouth cancer',
             'Floppy valve syndrome', 'Flu', 'Flu avian', 'Flu bird', 'Flu swine', 'Fluid around the heart',
             'Focal segmental glomerulosclerosis (FSGS)', 'Folate deficiency anemia', 'Folliculitis',
             'Food allergy',
             'Food allergy egg', 'Food allergy milk', 'Food poisoning', 'Food-borne illness', 'Foot drop',
             'Foot fracture', 'Foramen ovale', 'Fracture arm', 'Fracture greenstick', 'Fracture growth plate',
             'Fracture hip', 'Fracture incomplete', 'Fracture leg', 'Fracture stress', 'Fractured nose',
             'Fractured ribs', 'Frontal lobe epilepsy', 'Frontal lobe seizures', 'Frontotemporal dementia',
             'Frontotemporal lobar degeneration', 'Frostbite', 'Frozen shoulder', 'FSGS', "Fuchs' dystrophy",
             'Fugue dissociative', 'Functional dyspepsia', 'Functional neurologic disorders/conversion disorder',
             'Fungal infection nail', 'Funnel chest', 'GAD', 'Galactorrhea', 'Gallbladder cancer',
             'Gallbladder inflammation', 'Gallstones', 'Gambling compulsive', 'Ganglion cyst', 'Gangrene',
             'Gas and gas pains', 'Gastric cancer', 'Gastric emptying delayed', 'Gastric emptying rapid',
             'Gastritis',
             'Gastroenteritis viral', 'Gastroesophageal reflux', 'Gastroesophageal reflux disease (GERD)',
             'Gastrointestinal bleeding', 'Gastrointestinal stromal tumor (GIST)', 'Gastroparesis',
             'Gaucher disease',
             'Gender dysphoria', 'Gender identity disorder', 'Generalized anxiety disorder', 'Genital herpes',
             'Genital warts', 'Geographic tongue', 'Germ cell tumors', 'German measles', 'Gestational diabetes',
             'Giant cell arteritis', 'Giant lymph node hyperplasia', 'Giardia infection (giardiasis)',
             "Gilbert's syndrome", 'Gingivitis', 'Glaucoma', 'Glioblastoma', 'Glioma',
             'Globoid cell leukodystrophy',
             'Glomerulonephritis', 'Glossodynia', 'Glucocerebrosidase deficiency', 'Gluten-sensitive enteropathy',
             'Goiter', "Golfer's elbow", 'Gonorrhea', 'Gout', 'Grand mal seizure', 'Granuloma annulare',
             'Granulomatosis with polyangiitis', "Graves' disease", 'Greenstick fractures', 'Grief',
             'Gross hematuria',
             'Group B strep disease', 'Growing pains', 'Growth hormone excess', 'Growth plate fractures',
             'Guillain-Barre syndrome', 'Gum disease gingivitis', 'Gum disease periodontitis',
             'H. pylori infection',
             'H1N1 flu', 'H1N1 flu (swine flu)', 'H1N1v flu', 'H3N2v flu', 'Hair loss', 'Hair-pulling disorder',
             'Hairy cell leukemia', 'Hairy tongue', 'Halitosis', 'Hammertoeand mallet toe', 'Hamstring injury',
             'Hand fracture', 'Hand pain', 'Hand-foot-and-mouth disease', 'Hangovers',
             'Hantavirus pulmonary syndrome',
             'Hardening of the arteries', "Hashimoto's disease", 'Hay fever', 'Head and neck cancers', 'Head lice',
             'Head trauma coma', 'Headache chronic daily', 'Headache cluster', 'Headache exercise',
             'Headache external compression', 'Headache ice cream', 'Headache migraine', 'Headache primary cough',
             'Headache sex', 'Headache sinus', 'Headache spinal', 'Headache tension', 'Headache thunderclap',
             'Headaches in children', 'Health anxiety', 'Hearing loss', 'Heart arrhythmia', 'Heart attack',
             'Heart defects in adults', 'Heart disease', 'Heart failure', 'Heart murmurs', 'Heart palpitations',
             'Heart valve disease', 'Heartburn', 'Heat exhaustion', 'Heat rash', 'Heatstroke',
             'Heavy menstrual periods', 'Heel pain', 'Helicobacter pylori (H. pylori) infection', 'Hemangioma',
             'Hemangioma liver', 'Hematoma intracranial', 'Hematuria', 'Hemifacial spasm', 'Hemochromatosis',
             'Hemolytic uremic syndrome (HUS)', 'Hemophilia', 'Hemorrhoids', 'Henoch-Schonlein purpura',
             'Hepatitis A',
             'Hepatitis B', 'Hepatitis C', 'Hepatitis autoimmune', 'Hepatitis toxic', 'Hepatocellular carcinoma',
             'Hepatomegaly', 'Hepatopulmonary syndrome', 'Hereditary hemochromatosis',
             'Hereditary hemorrhagic telangiectasia', 'Hereditary motor and sensory neuropathy',
             'Hereditary nonpolyposis colorectal cancer syndrome', 'Hereditary progressive arthro-ophthalmopathy',
             'Hernia hiatal', 'Hernia inguinal', 'Hernia umbilical', 'Herniated disk', 'Herpes zoster',
             'Herpes zoster oticus', 'Herpes genital', 'Hiatal hernia', 'Hiccups', 'Hidradenitis suppurativa',
             'High blood pressure (hypertension)', 'High blood pressure in children',
             'High blood pressure secondary',
             'High cholesterol', 'High-flow priapism', 'Hilar cholangiocarcinoma', 'Hip dysplasia', 'Hip fracture',
             'Hip impingement', 'Hip labral tear', "Hirschsprung's disease", 'Hirsutism', 'Histoplasmosis',
             'HIV/AIDS',
             'Hives and angioedema', 'Hives chronic', 'Hoarding disorder', 'Hoarse voice', "Hodgkin's disease",
             "Hodgkin's lymphoma (Hodgkin's disease)", 'Hordeolum', 'Horner syndrome', 'Horner-Bernard syndrome',
             'Hot flashes', 'HPV infection', 'Human immunodeficiency virus', 'Human papillomavirus infection',
             'Hunchback', 'Hunter syndrome', "Huntington's disease", "Hunt's syndrome", 'Hurthle cell cancer',
             'Hutchinson-Gilford progeria syndrome', 'Hydrocele', 'Hydrocephalus', 'Hydronephrosis',
             'Hypercalcemia',
             'Hypercholesterolemia', 'Hypercholesterolemia familial', 'Hypercortisolism',
             'Hypereosinophilic syndrome',
             'Hyperglycemia in diabetes', 'Hyperhidrosis', 'Hypermenorrhea', 'Hyperopia',
             'Hyperoxaluria and oxalosis',
             'Hyperparathyroidism', 'Hypersexuality', 'Hypertension', 'Hypertension pregnancy-related',
             'Hypertension pulmonary', 'Hyperthyroidism (overactive thyroid)', 'Hypertrophic cardiomyopathy',
             'Hypoactive sexual desire disorder', 'Hypochondria', 'Hypoglycemia', 'Hypoglycemia diabetic',
             'Hypohidrosis', 'Hypohydration', 'Hyponatremia', 'Hypoparathyroidism', 'Hypopituitarism',
             'Hypoplastic left heart syndrome', 'Hypospadias', 'Hypotension', 'Hypothermia',
             'Hypothyroidism (underactive thyroid)', 'IBD', 'IBS', 'Ice cream headaches', 'Ichthyosis vulgaris',
             'Identity disorder dissociative', 'Idiopathic hypersomnia', 'Idiopathic intracranial hypertension',
             'Idiopathic myelofibrosis', 'Idiopathic thrombocytopenic purpura', 'Idiopathic toe walking',
             "IgA nephropathy (Berger's disease)", 'IgA vasculitis', 'IIH', 'Illness anxiety disorder',
             'Immune thrombocytopenia (ITP)', 'Immune thrombocytopenic purpura', 'Impacted wisdom teeth',
             'Impetigo',
             'Impotence', 'Incompetent cervix', 'Incomplete fracture', 'Incontinence bowel', 'Incontinence fecal',
             'Incontinence nighttime', 'Incontinence urinary', 'Indigestion', 'Infant jaundice', 'Infant reflux',
             'Infantile hemangioma', 'Infectious arthritis', 'Infectious diseases', 'Infertility',
             'Infertility female',
             'Infertility male', 'Inflammatory bowel disease (IBD)', 'Inflammatory breast cancer',
             'Inflammed gallbladder', 'Inflammed pancreas', 'Inflammed pericardium', 'Influenza (flu)',
             'Influenza avian', 'Influenza H1N1', 'Influenza swine flu', 'Ingrown hair', 'Ingrown toenails',
             'Inguinal hernia', 'Inherited metabolic disorder', 'Inherited metabolic disorders', 'Insomnia',
             'Insulin resistance syndrome', 'Intermittent explosive disorder', 'Interstitial cystitis',
             'Interstitial lung disease', 'Intestinal ischemia', 'Intestinal lipodystrophy',
             'Intestinal obstruction',
             'Intracranial hematoma', 'Intracranial venous malformations', 'Intraductal carcinoma',
             'Intrahepatic cholestasis of pregnancy', 'Intraocular melanoma', 'Intussusception',
             'Invasive lobular carcinoma', 'Iritis', 'Iron deficiency anemia', 'Iron overload',
             'Irritable bowel syndrome', 'Ischemia intestinal', 'Ischemic colitis', 'Ischemic priapism',
             'Islet cell cancer', 'Itchy skin (pruritus)', 'ITP', 'Jaw tumors and cysts', 'Jellyfish stings',
             'Jet lag disorder', 'Jock itch', 'Joint dislocation', "Jumper's knee", 'Juvenile fibromyalgia',
             'Juvenile idiopathic arthritis', 'Juvenile rheumatoid arthritis', 'Juvenile schizophrenia',
             "Kaposi's sarcoma", 'Kawasaki disease', 'Keratitis', 'Keratoconjunctivitis sicca', 'Keratoconus',
             'Keratosis pilaris', 'Keratosis actinic', 'Keratosis seborrheic', 'Ketoacidosis diabetic',
             'Kidney cancer',
             'Kidney cysts', 'Kidney disease chronic', 'Kidney failure acute', 'Kidney failure chronic',
             'Kidney infection', 'Kidney stones', 'Kissing disease', 'Klatskin tumor', 'Kleptomania',
             'Klinefelter syndrome', 'Klippel-Trenaunay syndrome', 'Knee bursitis', 'Knee pain', "Knee jumper's",
             'KP',
             'Krabbe disease', 'Kyphosis', 'Lactase deficiency', 'Lactation mastitis', 'Lactose intolerance',
             'Laryngitis', 'Lassa fever', 'Lateral elbow tendinopathy', 'Lateral epicondylitis',
             'Lateral epicondylosis', 'Latex allergy', 'Lazy eye (amblyopia)', 'LCIS', 'Lead poisoning',
             'Left ventricular hypertrophy', 'Leg fracture', 'Legg-Calve-Perthes disease', 'Legionellosis',
             "Legionnaires' disease", 'Leiomyosarcoma', 'Lentigines solar', 'Leukemia',
             'Leukemia acute lymphocytic',
             'Leukemia acute myelogenous', 'Leukemia chronic lymphocytic', 'Leukemia chronic myelogenous',
             'Leukemia general', 'Leukemia hairy cell', 'Leukoplakia', 'Lewy body dementia', 'Lice', 'Lice body',
             'Lichen nitidus', 'Lichen planus', 'Lichen planus oral', 'Lichen sclerosus',
             'Lichen simplex chronicus',
             'Limited scleroderma', 'Lip cancer', 'Lipodystrophy intestinal', 'Lipoma', 'Liposarcoma',
             'Listeria infection', 'Listeriosis', 'Lithiasis renal', 'Liver cancer', 'Liver disease',
             'Liver failure acute', 'Liver hemangioma', 'Liver spots', 'Liver enlarged',
             'Lobular carcinoma in situ (LCIS)', 'Lockjaw', 'Long QT syndrome', 'Loss of bladder control',
             "Lou Gehrig's disease", 'Lowblood pressure (hypotension)', 'Low blood sugar', 'Low body temperature',
             'Low sex drive in women', 'Low sperm count', 'Low testosterone', 'Low-flow priapism', 'Lung cancer',
             'Lung collapse', 'Lung disease interstitial', 'Lupus', 'Lupus nephritis', 'Lyme disease',
             'Lymph nodes swollen', 'Lymphadenitis', 'Lymphadenitis mesenteric', 'Lymphedema', 'Lymphoma',
             "Lymphoma Hodgkin's", "Lymphoma non-Hodgkin's", 'Lynch syndrome', 'Mad cow disease',
             'Major depressive disorder', 'Malaria', 'Male breast cancer', 'Male hypogonadism', 'Male infertility',
             'Malignant fibrous histiocytoma', 'Malignant hyperthermia', 'Malignant mesothelioma',
             'Malignant peripheral nerve sheath tumors', 'Mallet toe and hammertoe', 'Mammary duct ectasia',
             'Manic-depressive illness', 'Marburg virus', 'Marfan syndrome', 'Mastalgia', 'Mastitis',
             'MCAD deficiency',
             'MD', 'Measles', 'Measles German', 'Medial epicondylitis', 'Medial tibial stress syndrome',
             'Medication overuse headaches', 'Mediterranean anemia', 'Medulloblastoma', 'Megacolon',
             'Megaloblastic anemia', 'Melanoma', 'Melanoma of the eye', 'Membranous nephropathy',
             "Meniere's disease",
             'Meningioma', 'Meningitis', 'Meniscus tear', 'Menopause', 'Menorrhagia (heavy menstrual bleeding)',
             'Menstrual bleeding excessive', 'Menstrual cramps', 'Mental illness', 'Meralgia paresthetica',
             'Merkel cell carcinoma', 'Mesenteric ischemia', 'Mesenteric lymphadenitis', 'Mesothelioma',
             'Metabolic syndrome', 'Metachromatic leukodystrophy', 'Metastatic brain cancer', 'Metatarsalgia',
             'Methicillin-resistant staphylococcusaureus infection', 'MGUS', 'Microcephaly', 'Microscopic colitis',
             'Microscopic hematuria', 'Migraine', 'Migraine with aura', 'Mild cognitive impairment (MCI)', 'Milia',
             'Miliaria', 'Milkallergy', 'Milk intolerance', 'Miscarriage', 'Mitral valve disease',
             'Mitral valve prolapse', 'Mitral valve regurgitation', 'Mitral valve stenosis', 'Mittelschmerz',
             'Mixed connective tissue disease', 'Molar pregnancy', 'Mold allergy', 'Moles', 'Molluscum contagiosum',
             'Mono', 'Monoclonal gammopathy of undetermined significance (MGUS)', 'Mononucleosis', 'Mood disorders',
             'Morning sickness', 'Morphea', "Morton's neuroma", 'Mosquito bites', 'Mouth cancer',
             'Movement disorders',
             'Moyamoya disease', 'MRSA infection', 'MS', 'MSA', 'Mucocutaneous lymph node syndrome',
             'Mucopolysaccharidosis type II', 'Multiple endocrine neoplasia type 1',
             'Multiple endocrine neoplasia type 1 (MEN 1)', 'Multiple myeloma', 'Multiple personality disorder',
             'Multiple sclerosis', 'Multiple system atrophy (MSA)',
             'Multisystem inflammatory syndrome in children (MIS-C)', 'Mumps', 'Muscle cramp', 'Muscle strains',
             'Muscular dystrophy', 'Myasthenia gravis', 'Myelodysplastic syndromes', 'Myelofibrosis',
             'Myocardial infarction', 'Myocardial ischemia', 'Myocarditis', 'Myoclonus', 'Myofascial pain syndrome',
             'Myopia', 'Myxofibrosarcoma', 'Naegleria infection', 'Nail fungus',
             'Narcissistic personality disorder',
             'Narcolepsy', 'Nasal and paranasal tumors', 'Nasal polyps', 'Nasopharyngeal carcinoma',
             'Nearsightedness',
             'Neck pain', 'Nephroblastoma', 'Nephrogenic systemic fibrosis', 'Nephrotic syndrome',
             'Nervous system paraneoplastic syndromes', 'Neuralgia postherpetic', 'Neuralgia trigeminal',
             'Neuroblastoma', 'Neurodermatitis', 'Neuroendocrine carcinoma of the skin', 'Neuroendocrine tumors',
             'Neurofibroma', 'Neurofibromatosis', 'Neurofibrosarcoma', 'Neuroma acoustic', "Neuroma Morton's",
             'Neuroma plantar', 'Neuromyelitis optica', 'Neuromyelitis optica spectrum disorder',
             'Neuropathy autonomic', 'Neuropathy diabetic', 'Neuropathy hereditary motor and sensory',
             'Neuropathyperipheral', 'Nevi', 'Nevus', 'Nickel allergy', 'Nicotine addiction', 'Nicotine dependence',
             'Niemann-Pick', 'Nightmare disorder', 'Nighttime incontinence', 'Noctural enuresis',
             'Noise-related hearing loss', 'Nonalcoholic fatty liver disease', 'Nonallergic rhinitis',
             "Non-Hodgkin's lymphoma", 'Nonischemic priapism', 'Nonmelanoma skin cancer', 'Nontropical sprue',
             'Nonulcer dyspepsia', 'Noonan syndrome', 'Norovirus infection', 'Nose fracture', 'Novel coronavirus',
             'Nymphomania', 'Obesity', 'Obesity childhood', 'Obsessive-compulsive disorder (OCD)',
             'Obstetric cholestasis', 'Obstructive sleep apnea', 'Obstructive sleep apnea in children',
             'Occupational asthma', 'OCD', 'Ocular albinism', 'Ocular melanoma', 'Ocular rosacea',
             'Oculocutaneous albinism', 'Oculosympathetic palsy', 'ODD', 'Odontogenic tumors and cysts', 'OHSS',
             'Olfactory neuroblastoma', 'Oligodendroglioma', 'Onychomycosis', 'Oppositional defiant disorder (ODD)',
             'Optic neuritis', 'Oral cancer', 'Oral candidiasis', 'Oral lichen planus', 'Oral thrush', 'Orchitis',
             'Orthostatic hypotension (postural hypotension)', 'Osgood-Schlatter disease', 'Osteoarthritis',
             'Osteoarthritis cervical', 'Osteochondritis dissecans', 'Osteogenic sarcoma', 'Osteomalacia',
             'Osteomyelitis', 'Osteonecrosis', 'Osteophytes', 'Osteoporosis', 'Osteosarcoma', 'Otitis externa',
             'Otitis media', 'Outer ear infection', 'Ovarian cancer', 'Ovarian cysts',
             'Ovarian hyperstimulation syndrome', 'Overactive bladder', 'Overactive thyroid',
             'Oxyphil cell carcinoma',
             'PAD', 'PAES', "Paget's disease of bone", "Paget's disease of the breast",
             "Paget's disease of the nipple",
             'Pain chest', 'Pain wrist', 'Painful bladder syndrome', 'Painful intercourse (dyspareunia)',
             'Painful periods', "Palsy Bell's", 'Palsy cerebral', 'Palsy facial', 'Palsy progressive supranuclear',
             'Pancreas inflammation', 'Pancreatic cancer', 'Pancreatic cysts', 'Pancreatic neuroendocrine tumors',
             'Pancreatitis', 'Panic attacks and panic disorder', 'PAPVR', 'Paraganglioma',
             'Paraneoplastic syndromes',
             'Paraneoplastic syndromes of the nervous system', 'Paranoid personality disorder', 'Paraplegia',
             "Parkinson's disease", 'Parotid tumors', 'Partial anomalous pulmonary venous connection',
             'Partial anomalous pulmonary venous return', 'Parvovirus infection', 'Patellar tendinitis',
             'Patellofemoral pain syndrome', 'Patent ductus arteriosus (PDA)', 'Patent foramen ovale',
             'Pathological gambling', 'Pathological laughter and crying', 'Pathological stealing', 'PBA', 'PCOS',
             'PDA',
             'Peanut allergy', 'Pectus carinatum', 'Pectus excavatum', 'Pediatric brain tumors',
             'Pediatric obstructive sleep apnea', 'Pediatricthrombocytopenia',
             'Pediatric white blood cell disorders',
             'Pediculosis capitis', 'Pelvic inflammatory disease (PID)', 'Pelvic organ prolapse',
             'Pelvic pain chronic',
             'Pelvic support problems uterine prolapse', 'Pemphigus', 'Penicillin allergy', 'Peptic ulcer',
             'Perforated eardrum', 'Pericardial effusion', 'Pericardial inflammation', 'Pericarditis',
             'Perimenopause',
             'Periodontal disease gingivitis', 'Periodontal disease periodontitis', 'Periodontitis',
             'Peripheral artery disease (PAD)', 'Peripheral nerve injuries', 'Peripheral nerve tumors',
             'Peripheral neuropathy', 'Peripheral vascular disease', 'Peritonitis', 'Pernicious anemia', 'Pernio',
             'Peroneal muscular atrophy', 'Persistent depressive disorder (dysthymia)',
             'Persistent post-concussive symptoms (Post-concussion syndrome)', 'Personality disorder antisocial',
             'Personality disorder borderline', 'Personality disorder narcissistic',
             'Personality disorder schizoid',
             'Personality disorder schizotypal', 'Personality disorders', 'Pertussis', 'Pes planus', 'Pet allergy',
             'Petit mal seizure', "Peyronie's disease", 'Phantom pain', 'Pharyngitis', 'Phenylketonuria (PKU)',
             'Pheochromocytoma', 'Phlebitis', 'Phobia social', "Pick's disease", 'PID', 'Piles', 'Pilonidal cyst',
             'Pilonidal dimple', 'Pimples', 'Pinched nerve', 'Pineoblastoma', 'Pink eye (conjunctivitis)',
             'Pinworm infection', 'Pituitary insufficiency', 'Pituitary tumors', 'Pityriasis rosea',
             'Pityriasis versicolor', 'PKD', 'PKU', 'Placenta accreta', 'Placenta previa', 'Placental abruption',
             'Plague', 'Plantar fasciitis', 'Plantar neuroma', 'Plantar warts', 'Pleurisy', 'Pleuritis', 'PLS',
             'Pneumonia', 'Pneumonitis', 'Pneumothorax', 'POEMS syndrome', 'Poison ivy rash', 'Polio',
             'Polycystic kidney disease', 'Polycystic ovary syndrome (PCOS)', 'Polycythemia vera', 'Polyhydramnios',
             'Polymorphous light eruption', 'Polymyalgia rheumatica', 'Polymyositis', 'Polyps colon',
             'Polyps endometrial', 'Polyps nasal', 'Polyps stomach', 'Polyps uterine', 'Pompholyx',
             'Poor color vision',
             'Popliteal artery aneurysm', 'Popliteal artery entrapment syndrome', 'Popliteal cyst', 'Porphyria',
             'Post-cardiac injury syndrome', 'Post-chemotherapy cognitive impairment', 'Posterior cortical atrophy',
             'Posterior cruciate ligament injury', 'Posterior prolapse', 'Posterior vaginal prolapse (rectocele)',
             'Postherpetic neuralgia', 'Postmyocardial infarction syndrome', 'Postpartum depression',
             'Postpartum hypopituitarism', 'Postpartum preeclampsia', 'Postpartum thyroiditis',
             'Post-polio syndrome',
             'Post-traumatic stress disorder (PTSD)', 'Postural hypotension', 'Pouchitis',
             'Prader-Labhart-Willi syndrome', 'Prader-Willi syndrome', 'Precocious puberty', 'Prediabetes',
             'Preeclampsia', 'Preexcitation syndrome', 'Pregnancy-related hypertension', 'Premature birth',
             'Premature ejaculation', 'Premature ovarian failure', 'Premature puberty',
             'Premature ventricular contractions (PVCs)', 'Premenstrual syndrome', 'Premenstrual syndrome (PMS)',
             'Presbycusis', 'Presbyopia', 'Prescription drug abuse', 'Pressure injury', 'Pressure sores',
             'Pressure ulcer', 'Preterm labor', 'Priapism', 'Prickly heat', 'Primary adrenal insufficiency',
             'Primary aldosteronism', 'Primary biliary cholangitis', 'Primary biliary cirrhosis',
             'Primary hypoaldosteronism', 'Primary immunodeficiency', 'Primary lateral sclerosis (PLS)',
             'Primary ovarian insufficiency', 'Primary polycythemia', 'Primary progressive aphasia',
             'Primary sclerosing cholangitis', 'Proctitis', 'Progeria', 'Progressive supranuclear palsy',
             'Prolactinoma', 'Prolapse mitral valve', 'Prolapsed bladder', 'Prolapsed uterus', 'Prostate cancer',
             'Prostate gland enlargement', 'Prostatitis', 'Pruritis ani', 'Pruritus', 'Pseudobulbar affect',
             'Pseudocholinesterase deficiency', 'Pseudogout', 'Pseudomembranous colitis', 'Pseudotumor cerebri',
             'Psoriasis', 'Psoriatic arthritis', 'Psychosis', 'PTSD', 'Pubic lice (crabs)', 'Puffy eyes',
             'Pulmonary atresia', 'Pulmonary atresia with intact ventricular septum',
             'Pulmonary atresia with ventricular septum defect', 'Pulmonary edema', 'Pulmonary embolism',
             'Pulmonary fibrosis', 'Pulmonary hypertension', 'Pulmonary valve disease', 'Pulmonary valve stenosis',
             'PVCs', 'PVD', 'Pyelonephritis', 'Pyloric stenosis', 'Pyoderma gangrenosum', 'Q fever', 'Quadriplegia',
             'Query fever', 'Rabbit fever', 'Rabies', 'Radiation enteritis', 'Radiation sickness',
             'Ramsay Hunt syndrome', 'Rapid gastric emptying', 'Rapid heartbeat', 'Rash poison ivy',
             "Raynaud's disease", 'Reactive arthritis', 'Reactive attachment disorder',
             'Reading disability specific',
             'Rebound headache', 'Rectal cancer', 'Rectal inflammation', 'Rectal itching', 'Rectal prolapse',
             'Rectal ulcer', 'Rectovaginal fistula', 'Recurrent breast cancer', 'Red eye', 'Reflux bile',
             'Reflux gastroesophageal', 'Reflux vesicoureteral', 'Regurgitation aortic valve',
             'Regurgitation mitral valve', "Reiter's syndrome", 'REM sleep behavior disorder',
             'Renal artery stenosis',
             'Renal cancer', 'Renal failure acute', 'Renal lithiasis', 'Residual limb pain',
             'Respiratory syncytialvirus (RSV)', 'Restless legs syndrome', 'Retinal detachment', 'Retinal diseases',
             'Retinoblastoma', 'Retinopathy diabetic', 'Retractile testicle', 'Retrograde ejaculation',
             'Rett syndrome',
             "Reye's syndrome", 'Rhabdomyosarcoma', 'Rheumatic fever', 'Rheumatoid arthritis', 'Rhinitis allergic',
             'Rhinitis nonallergic', 'Rhinitis vasomotor', 'Rib fracture', 'Rickets', 'Rift Valley fever',
             'Ringing in the ear', 'Ringworm (body)', 'Ringworm (scalp)', 'Ringworm of the foot', 'RLS',
             'Road rage',
             'Rocky Mountain spotted fever', 'Rosacea', 'Roseola', 'Rotator cuff injury', 'Rotavirus', 'Round back',
             'RSV', 'Rubella', 'Rubeola', 'Rumination syndrome', "Runner's knee",
             'Ruptured eardrum (perforated eardrum)', 'Ruptured spleen', 'Sacral dimple', 'Sacroiliitis', 'SAD',
             'Salivary gland tumors', 'Salmonella infection', 'Salmonellosis', 'Sarcoidosis', 'Sarcoma',
             'Sarcoma bone cancer', 'Sarcoma soft tissue', 'SBBO', 'Scabies', 'SCAD', 'Scalded mouth syndrome',
             'Scarlatina', 'Scarlet fever', 'Schizoaffective disorder', 'Schizoid personality disorder',
             'Schizophrenia', 'Schizophrenia adolescent', 'Schizophrenia childhood', 'Schizophrenia juvenile',
             'Schizotypal personality disorder', 'Schwannoma', 'Sciatica', 'Scleroderma', 'Scleroderma limited',
             'Sclerosing cholangitis', 'Sclerosing mesenteritis', 'Sclerosis amyotrophic lateral',
             'Sclerosis multiple',
             'Sclerosis systemic', 'Scoliosis', 'Scorpion sting', 'Scrotal masses',
             'Seasonal affective disorder (SAD)',
             'Seasonalallergy', 'Sebaceous carcinoma', 'Sebaceous cysts', 'Seborrheic dermatitis',
             'Seborrheic keratosis', 'Secondary brain cancer', 'Secondary hypertension', 'Seizure disorder',
             'Seizure absence', 'Seizure febrile', 'Seizure grand mal', 'Seizure petit mal',
             'Seizure temporal lobe',
             'Seizures', 'Selective IgA deficiency', 'Self harming', 'Self-injury/cutting', 'Separated shoulder',
             'Separation anxiety disorder', 'Sepsis', 'Septal defect atrial', 'Septal defect atrioventricular',
             'Septal defect ventricular', 'Septic arthritis', 'Serotonin syndrome',
             'Severe acute respiratory syndrome',
             'Severe acute respiratory syndrome (SARS)', 'Severe brain injury coma', 'Sex headaches',
             'Sexual dysfunction female', 'Sexual obsession', 'Sexually transmitted diseases (STDs)',
             'Shaken baby syndrome', "Sheehan's syndrome", 'Shellfish allergy', 'Shigella infection',
             'Shin splints',
             'Shingles', 'Short bowel syndrome', 'Shoulder dislocation', 'Shoulder separation',
             'Shy-Drager syndrome',
             'SIBO', 'Sick sinus syndrome', 'Sickle cell anemia', 'SIDS', 'Sin Nombre virus infection',
             'Sinus headaches', 'Sinusitis acute', 'Sinusitis chronic', "Sjogren's syndrome", 'Skin cancer',
             'Skin cancer melanoma', 'Skin dry', 'Skin itchy', 'Skipped heartbeats', 'Slapped cheek disease',
             'Sleep apnea', 'Sleep apnea in children obstructive', 'Sleep apnea central', 'Sleep apnea obstructive',
             'Sleep disorders', 'Sleep terrors', 'Sleep terrors (night terrors)', 'Sleepiness daytime',
             'Sleeplessness',
             'Sleep-related eating disorder', 'Sleepwalking', 'Slipped disk', 'Slow heartbeat',
             'Small bowel bacterial overgrowth', 'Small bowel cancer', 'Small bowel prolapse',
             'Small bowel prolapse (enterocele)', 'Small intestinal bacterial overgrowth (SIBO)',
             'Small intestine prolapse', 'Small vessel disease', 'Smallpox', 'Snoring',
             'Social anxiety disorder (social phobia)', 'Soft palate cancer', 'Soft tissue sarcoma',
             'Solar keratosis',
             'Solar lentigines', 'Solitary fibrous tumor', 'Solitary rectal ulcer syndrome',
             'Somatic symptom disorder',
             'Somnambulism', 'Sore throat', 'Soy allergy', 'Spasmodic torticollis', 'Specific phobias',
             'Specific reading disability', 'Spermatocele', 'Spider bites', 'Spina bifida',
             'Spinal arteriovenous malformation (AVM)', 'Spinal cord injury', 'Spinal cord tumor',
             'Spinal curvature',
             'Spinal headaches', 'Spinal stenosis', 'Splenomegaly', 'Spondylosis cervical',
             'Spontaneous coronary artery dissection (SCAD)', 'Sprained ankle', 'Sprains',
             'Squamous cell carcinoma of the skin', 'Stage 4 prostate cancer', 'Stammering', 'Staph infections',
             'STDs',
             'Steele-Richardson-Olszewski syndrome', 'Stein-Leventhal syndrome', 'Stenosing tenosynovitis',
             'Stenosis aortic valve', 'Stenosis mitral valve', 'Stenosis pulmonary valve', 'Stenosis pyloric',
             'Stenosis spinal', 'Stevens-Johnson syndrome', 'Stickler syndrome', 'Stings bee', 'Stings jellyfish',
             'Stings scorpion', 'Stomach cancer', 'Stomach flu', 'Stomach pain nonulcer', 'Stomach polyps',
             'Stomatodynia', 'Stones kidney', 'Stool holding', 'Strawberry hemangioma', 'Strep throat',
             'Stress cardiomyopathy', 'Stress fractures', 'Stress incontinence', 'Stretch marks', 'Stroke',
             'Stump pain', 'Stuttering', 'Sty', 'Subarachnoid hemorrhage',
             'Subconjunctival hemorrhage (broken blood vessel in eye)', 'Subdural hematoma', 'Subfertility',
             'Sudden cardiac arrest', 'Sudden infant death syndrome (SIDS)', 'Suicide',
             'Suicide and suicidal thoughts',
             'Sun allergy', 'Sun poisoning', 'Sunburn', 'Sunken chest', 'Supraventricular tachycardia',
             'Suspicious breast lumps', 'SVT', 'Sweating and body odor', 'Sweating abnormally excessive',
             "Sweet's syndrome", "Swimmer's ear", "Swimmer's itch", 'Swollen knee', 'Swollen lymph nodes',
             'Syncope vasovagal', 'Syndrome X', 'Synostosis', 'Synovial sarcoma', 'Syphilis', 'Syringomyelia',
             'Systemic capillary leak syndrome', 'Systemic lupus erythematosus', 'Systemic mastocytosis',
             'Systemic sclerosis', 'Tachycardia', "Takayasu's arteritis", 'Takotsubo cardiomyopathy',
             'Tapeworm infection', 'TAPVR', 'Tay-Sachs disease', 'TB', 'Tears decreased production',
             'Teen depression',
             'Teeth grinding', 'Temporal arteritis', 'Temporal lobe seizure', 'Temporomandibular disorders',
             'Temporomandibular joint disorders', 'TEN', 'Tendinitis', 'Tendinitis Achilles', 'Tendinitis patellar',
             'Tennis elbow', "Tenosynovitis de Quervain's", 'Tension headache', 'Testicle retractile',
             'Testicle undescended', 'Testicular cancer', 'Testicular torsion', 'Testosterone deficiency',
             'Tetanus',
             'Tetralogy of Fallot', 'Tetraplegia', 'TGA', 'Thalassemia', 'Thoracic aortic aneurysm',
             'Thoracic outlet syndrome', 'Three-day measles', 'Throat cancer', 'Thromboangiitis obliterans',
             'Thrombocythemia essential', 'Thrombocytopenia (low platelet count)', 'Thrombocytopenia childhood',
             'Thrombocytosis', 'Thrombophlebitis', 'Thrush oral', 'Thumb arthritis', 'Thunderclap headaches',
             'Thyroid cancer', 'Thyroid gland enlargement', 'Thyroid nodules', 'Thyroid overactive',
             'Thyroid underactive', 'Thyroiditis chronic lymphocytic', 'TIA', 'Tic douloureux', 'Tinea barbae',
             'Tinea capitis', 'Tinea corporis', 'Tinea cruris', 'Tinea pedis', 'Tinea versicolor', 'Tinnitus',
             'TMJ disorders', 'Toe walking in children', 'Toenail fungus', 'Tongue cancer', 'Tongue tie',
             'Tongue-tie (ankyloglossia)', 'Tonic-clonic seizure', 'Tonsil cancer', 'Tonsillitis', 'Tooth abscess',
             'Tooth decay', 'Torn meniscus', 'Torsion testicular', 'Torticollis spasmodic',
             'Total anomalous pulmonary venous connection', 'Total anomalous pulmonary venous return',
             'Tourette syndrome', 'Toxemia', 'Toxic epidermal necrolysis', 'Toxic hepatitis',
             'Toxic shock syndrome',
             'Toxoplasmosis', 'Trachoma', 'Transient global amnesia', 'Transient ischemic attack (TIA)',
             'Transposition of great vessels', 'Transposition of the great arteries', 'Transverse myelitis',
             'Traumatic brain injury', 'Traumatic grief', "Traveler's diarrhea", 'Trichinosis', 'Trichomoniasis',
             'Trichotillomania (hair-pulling disorder)', 'Tricuspid atresia', 'Tricuspid valve disease',
             'Tricuspid valve regurgitation', 'Trigeminal neuralgia', 'Trigger finger', 'Triple X syndrome',
             'Trisomy 21 syndrome', 'Trisomy X', 'Trouble swallowing', 'Truncus arteriosus',
             'Trypanosomiasis American',
             'Tuberculosis', 'Tuberous sclerosis', 'Tularemia', 'Tumor salivary gland', 'Turner syndrome',
             'Type 1 diabetes', 'Type 1 diabetes in children', 'Type 2 diabetes', 'Type 2 diabetes in children',
             'Typhoid fever', 'Ulcer aphthous', 'Ulcer peptic', 'Ulcer rectal', 'Ulcerative colitis',
             'Ulnar wrist pain', 'Umbilical hernia', 'Uncontrollable laughter and crying', 'Underactive thyroid',
             'Under-eye puffiness', 'Undescended testicle', 'Undifferentiated pleomorphic sarcoma', 'Upset stomach',
             'Ureteral cancer', 'Ureteral obstruction', 'Urethral stricture', 'Urinary incontinence',
             'Urinary tract infection', 'Urinary tract infection (UTI)', 'Urine color', 'Urine blood in',
             'Urticaria',
             'Uterine cancer', 'Uterine fibroids', 'Uterine leiomyoma', 'Uterine myoma', 'Uterine polyps',
             'Uterine prolapse', 'Uterus didelphys', 'Uveal melanoma', 'Uveitis', 'Vaginal agenesis',
             'Vaginal atrophy',
             'Vaginal cancer', 'Vaginal candidiasis', 'Vaginal fistula', 'Vaginal prolapse posterior', 'Vaginitis',
             'Valley fever', 'Valvular heart disease', 'Variant CJD', 'Varicella', 'Varices esophageal',
             'Varicocele',
             'Varicose veins', 'Variola', 'Vascular dementia', 'Vascular rings', 'Vasculitis', 'Vasomotor rhinitis',
             'Vasovagal syncope', 'vCJD', 'Velocardiofacial syndrome', 'Venereal warts', 'Ventricular fibrillation',
             'Ventricular premature contraction', 'Ventricular septal defect (VSD)', 'Ventricular tachycardia',
             'Vertebral tumor', 'Vertigo', 'Vesicoureteral reflux', 'Vestibular schwannoma', 'V-fib',
             'Viral gastroenteritis (stomach flu)', 'Viral hemorrhagic fevers', 'Vitamin deficiency anemia',
             'Vitiligo',
             'Vocal cord paralysis', 'Vocal fold paralysis', 'Voice disorders', 'Von Willebrand disease', 'VPCs',
             'Vulvar cancer', 'Vulvodynia', 'Waldenstrom macroglobulinemia', 'Warts common', 'Warts genital',
             'Warts plantar', 'Warts venereal', 'Water on the knee', "Wegener's granulomatosis", 'Weight loss',
             'Wermer syndrome', "Wermer's syndrome", 'West Nile virus', 'Wet macular degeneration', 'Wheat allergy',
             'Whiplash', "Whipple's disease", 'White blood cell disorders in children', 'Whiteheads',
             'Whooping cough',
             "Wilms' tumor", "Wilson's disease", 'Wisdom teeth impacted', 'Wolff-Parkinson-White (WPW) syndrome',
             'Wrinkles', 'Wrist fracture', 'Wrist pain', 'X Syndrome', 'Xerosis', 'Xerostomia',
             'X-linked agammaglobulinemia', 'XXX syndrome', 'Yeast infection (vaginal)', 'Yellow fever',
             'Yersinia pestis', 'Yips', 'Zika virus', 'Zollinger-Ellison syndrome', 'Zoster']
    if driver.flag == 0 and user_input.lower()!= 'no':
        bot_response = ''
        response_flag = 0
        greetings = ['hi', 'hello', 'hay']
        if user_input in greetings:
            bot_response = bot_response + ' ' + 'Hello !!!!!!!   Enter ur question'
            response_flag = 1

        if 'my symptoms are' in user_input:
            user_input.replace('my symptoms are', '')
            # print('in')
            list1 = []
            conn = sqlite3.connect('disease_details.db')
            cur = conn.cursor()
            cur.execute("SELECT Symptoms FROM disease_info  ")
            conn.commit()
            dis = cur.fetchall()
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
            # print(range(len(symp)), symp)
            symp.reverse()
            for i in range(len(symp)):
                driver.symp.append(symp[i])
                if i > 5:
                    break
            # print(str(k * 100) + '% Match')

            conn = sqlite3.connect('disease_details.db')
            cur = conn.cursor()
            cur.execute("SELECT Disease_name FROM disease_info  WHERE Symptoms= ? ", (bot_response,))
            conn.commit()
            dis_nm = cur.fetchall()
            for i in dis_nm:
                for j in i:
                    bot_response = j
            driver.diseasename=bot_response
            response_flag = 1
            return (bot_response)

        names.append(user_input)
        cn = CountVectorizer().fit_transform(names)
        similarity_scores_names = cosine_similarity(cn[-1], cn)
        similarity_scores_list = similarity_scores_names.flatten()
        index1 = index_sort(similarity_scores_list)
        index1 = index1[1:]
        max = 0.0
        name = ''
        for i in range(len(index1)):
            if similarity_scores_list[index1[i]] > max:
                name = names[index1[i]]
                max = similarity_scores_list[index1[i]]
                response_flag = 1
        names.remove(user_input)

        driver.diseasename = name

        if response_flag== 1:
            list1=''
            conn = sqlite3.connect('disease_details.db')
            cur = conn.cursor()
            s = "SELECT Symptoms FROM disease_info  where Disease_name='" + str(driver.diseasename) + "'"
            cur.execute(s)
            dis = cur.fetchall()
            for i in dis:
                for j in i:
                    list1=list1+''+str(j)
                    print(j)
                    print(list1)
            list1 = list(map(str, list1.split('$$')))
            list1 = list(filter(('').__ne__, list1))
            print(list1)
            # print(range(len(symp)), symp)
            list1.reverse()
            for i in range(len(list1)):
                driver.symp.append(list1[i])
                if i > 5:
                    break
            print(list1,driver.symp)
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


            for i in range(len(index1)):
                if similarity_scores_list[index1[i]] > max:
                    term = terms[index1[i]]
                    max = similarity_scores_list[index1[i]]
            # print(name,terms1[terms.index(term)])
            if term != 'Overview':
                term = terms1[terms.index(term)]
            terms.remove(user_input)
            conn = sqlite3.connect('disease_details.db')
            cur = conn.cursor()
            s = "SELECT " + str(term) + " FROM disease_info  where Disease_name='" + str(name) + "'"
            cur.execute(s)
            res1 = ''
            for i in cur.fetchall():
                for j in i:
                    res1 = res1 + str(j)
                    # print(res1)
            res = list(map(str, res1.split('$$')))
            res = list(filter(('').__ne__, res))
            final = ''
            for i in range(len(res)):
                if 'Open pop-up dialog box Close' in res[i]:
                    continue
                else:
                    final = final + str(res[i])
            response_flag=1
            return (final)

        if response_flag == 0 :
            bot_response = bot_response + ' ' + 'i did not understand'

        return bot_response
    if driver.flag == 2:
        questions = ["Name: ", " AGE: ", "Gender: ","PHONE NUMBER: ", "Name of the disease: ", "Name of the doctor: ", "Symptoms: "]
        if driver.flag == 2 and driver.i == 0:
            response = response + ' ' + questions[driver.i]
            driver.i += 1
            return response

        if driver.flag == 2 and driver.i == 1:
            driver.username = user_input
            driver.filename = driver.username + '.txt'
            if not os.path.exists(driver.filename):
                create_file(driver.filename)
                write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
                today = date.today()
                today = str(today)
                write_to_file(driver.filename, "DATE OF REGISTRATION : " + today)
                driver.filechecker = 1
                response = response + ' ' + questions[driver.i]
                write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
                driver.i += 1
                return response

            else:
                write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
                driver.i = 3
                today = date.today()
                today = str(today)
                write_to_file(driver.filename, "DATE OF REGISTRATION : " + today)
                response = response + ' ' + questions[driver.i]
                driver.i += 1
                return response
        if (driver.flag == 3 and driver.i == 2) or (driver.i == 2 and driver.filechecker == 1):
            response = response + ' ' + questions[driver.i]
            write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
            driver.i += 1
            return response

        if (driver.flag == 2 and driver.i == 3) or (driver.i == 3 and driver.filechecker == 1):
            response = response + ' ' + questions[driver.i]
            write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
            driver.i += 1
            return response

        if driver.flag == 2 and driver.i == 4:
            # response = response + ' ' + questions[driver.i]
            write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
            driver.i += 1
            # return response

        if driver.flag == 2 and driver.i == 5:
            # response = response + ' ' + questions[driver.i]
            write_to_file(driver.filename, questions[driver.i - 1] + " " + driver.diseasename)
            driver.i += 1
            # return response

        if driver.flag == 2 and driver.i == 6 :
            response = response + ' ' + questions[driver.i]
            write_to_file(driver.filename, questions[driver.i - 1] + " " + driver.docname)
            driver.i += 1
            if driver.symp[0]=='No record':
                driver.i=10
            return response
        if driver.flag == 2 and driver.i == 10:
            write_to_file(driver.filename, questions[7] + " " + user_input)
            driver.i = 8

        if driver.flag == 2 and driver.i == 7:
            if driver.i==7 and driver.s==0:
                print(driver.symp)
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename,questions[driver.i - 1] + " " + user_input)
                driver.s += 1
                return response
            if driver.i==7 and driver.s==1:
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename, driver.symp[driver.s-1] + " " + user_input)
                driver.s += 1
                return response
            if driver.i==7 and driver.s==2:
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename, driver.symp[driver.s-1] + " " +user_input)
                driver.s += 1
                return response
            if driver.i==7 and driver.s==3:
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename, driver.symp[driver.s-1] + " " + user_input)
                driver.s += 1
                return response
            if driver.i==7 and driver.s==4:
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename, driver.symp[driver.s-1] + " " + user_input)
                driver.s += 1
                return response
            if driver.i==7 and driver.s==5:
                response = response + 'Please tpye "YES" if you the following symptoms or type "NO"'
                response = response +str('</p><p class="botText"><span>') + driver.symp[driver.s]
                write_to_file(driver.filename, driver.symp[driver.s-1] + " " + user_input)
                driver.s += 1
                driver.i += 1
                return response


        if driver.flag == 2 and driver.i == 8:
            response = response + ' ' + 'would you like to book a appointment '
            write_to_file(driver.filename,  driver.symp[driver.s-1] + " " + user_input)
            write_to_file(driver.filename, "\n" + ' *************************************************** ' + "\n ")
            driver.i += 1
            return response
        if driver.flag == 2 and driver.i == 9:
            response = response + ' ' + 'would you like to book a appointment '
            write_to_file(driver.filename, questions[driver.i - 1] + " " + user_input)
            write_to_file(driver.filename, "\n" + ' *************************************************** ' + "\n ")
            driver.i += 1
            return response1
    if driver.flag == 3:
        if driver.k == 0:
            string= 'Enter the date:'
            driver.k+=1
            return string
        if driver.k == 1:
            driver.date=user_input
            string='Enter the time:'
            driver.k += 1
            return string
        if driver.k == 2:
            driver.time= user_input
            email_user = os.environ.get('EMAIL')
            email_password = os.environ.get('EMAIL_PASS')
            email_send = 'kr737111@gmail.com'

            subject = 'Apponitment Booking'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject

            body = f'''Hello! I am {driver.username}.
                    I want to book  a real time appointment with you regarding {driver.diseasename}
                    *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
                    Apponitment details:
                    Date : {driver.date}
                    Time : {driver.time}
                    Patient name : {driver.username}
                    Doctor Name : {driver.docname}
                    Contact info : Provided in the attachment 
                    *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
                    
                    Thanks And Regards,
                    {driver.username}
                    '''
            msg.attach(MIMEText(body, 'plain'))

            filename = driver.filename
            attachment = open(filename, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()
            response = response + ' ' + 'Appointment booking succesfull, Email is sent '+str('</p><p class="botText"><span>') +'Thanks for using our services'
            return response
    if user_input.lower() == 'no':
        if driver.flag==2 and driver.i==7 and driver.s<=5:
            pass
        if driver.flag == 0:
            string = 'Would u like to know about more '+ str(driver.diseasename) +str('</p><p class="botText"><span>') +'OR'+str('</p><p class="botText"><span>')+'You can also know about these disease by typing there name '+str('</p><p class="botText"><span>')+str(random.choice(names))+str('</p><p class="botText"><span>') +str(random.choice(names))+str('</p><p class="botText"><span>')+str(random.choice(names))
            return string
        if driver.flag == 1:
            string = 'The form will help the doctor understand about your condition' +str('</p><p class="botText"><span>') +'Please type "yes" to continue'
            return string
        if driver.flag == 2:
            string =str(driver.docname) + ' will help you to get better' + str('</p><p class="botText"><span>') + 'Please type "yes" to continue'
            return string


disease = Blueprint("disease", __name__, static_folder="static", template_folder="templates/disease")


def sug1(static=None):
    global response
    time.sleep(4)
    if driver.flag == 0 and driver.j == 0 :
        response = 'You can also learn about the symptoms ,causes and  risks by typing (symptoms or risks or casues) of (disease name)'
        driver.j=1
    elif driver.flag == 0 and driver.j == 1 :
        response ='Would u like to contact doctor for '+str(driver.diseasename)+' ?'
    if driver.flag == 1:
        response = 'please type "yes" to fill a form and continue with appointment '
    return response


@disease.route("/")
def home():
    return render_template("disease.html")


@disease.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if driver.flag == 0 and userText.lower()!='no':
        return str(bot_response(userText)) + str('</p><p class="botText"><span>') + str(sug()) + str('</span>')
    else:
        return str(bot_response(userText))


# @disease.route("/sug")
def sug():
    x = sug1()
    return str(x)
