#--This file is for comparing SVM, Logistic Regression, and MultimonialNB models--#
#--Import libraries--#
import pandas as pd
from SVM import support_vector_machine
from LoadSpamHamData import load_spam_ham_data
from MultimonialNB import mulmonial_naive_bayes
from sklearn.model_selection import train_test_split
from LogisticRegression import logistic_regression_model
#--Load Data--#
file_path = "../Data/SpamHamDataset01.csv"
df = load_spam_ham_data(file_path)

if df is not None:
    #--Split data--#
    X_train, X_test, Y_train, Y_test = train_test_split(
        df['content'], df['label'], test_size=0.2, random_state=42
    )
    print(f"[*] Total Data: {len(df)} rows. Running Models Comparison...\n")
    #--Collect Results--#
    results = []
    #--Call def od each model and paste to result--#
    print("[>] Processing Multinomial NB...")
    results.append({"Model": "Multinomial NB", **mulmonial_naive_bayes(X_train, X_test, Y_train, Y_test)})
    print("[>] Processing Linear SVM...")
    results.append({"Model": "Lninear SVM", **support_vector_machine(X_train, X_test, Y_train, Y_test)})
    print("[>] Processing Logistic Reg...")
    results.append({"Model": "Logistic Reg", **logistic_regression_model(X_train, X_test, Y_train, Y_test)})
    #--Print Professional Comparison Table--#
    print("\n" + "╔" + "═"*98 + "╗")
    print(f"║ {'SPAM DETECTION PERFORMANCE BENCHMARK':^98} ║")
    print("╠" + "═"*22 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╦" + "═"*12 + "╣")
    print(f"║ {'ALGORITHM':<22} ║ {'ACCURACY':^10} ║ {'PRECISION':^10} ║ {'RECALL':^10} ║ {'F1-SCORE':^10} ║ {'TIME (S)':^10} ║")
    print("╠" + "═"*22 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╬" + "═"*12 + "╣")
    for r in results:
        print(f"║ {r['Model']:<22} ║ {r['acc']:^10.2%} ║ {r['p']:^10.2%} ║ {r['r']:^10.2%} ║ {r['f1']:^10.2%} ║ {r['time']:^10.4f} ║")
    
    print("╚" + "═"*22 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╩" + "═"*12 + "╝")
    #--Determine the most powerful model--#
    winner = max(results, key=lambda x: x['f1'])
    print(f"\n🏆 FINAL VERDICT: The most effective model is {winner['Model']} with an F1-Score of {winner['f1']:.2%}.")