import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv("C:/Users/acer/OneDrive/Desktop/visco file/tudent Marks Analyzer  start a projects/data/students.csv")
# # print("ORIGINAL DATA ")
# # print(df)
# # print("/n missing value")
# # print(df.isnull().sum())
# # print("\n dupilcate value")
# # print(df.duplicated().sum())
subjects = ["Python", "SQL", "Java", "Maths"]
# # calculate Total
# df['total']=df[subjects].sum(axis=1)

# # average
# df['average']=df[subjects].mean(axis=1)

# # calculate percentage
# df['percentage']=(df['total']/(len(subjects)*100))*100


# # grade function
# def grade_calculate(percentage2):
#     if percentage2 >=90:
#         return "A+"
#     elif percentage2 >=80:
#         return "A"
#     elif percentage2 >=70:
#         return "B+"
#     elif percentage2 >=60:
#         return "B"
#     elif percentage2 >=50:
#         return "C"
#     elif percentage2 >=40:
#         return "D"
#     else:
#         return "RA"
# df['grade']=df["percentage"].apply(grade_calculate)



# # apply pass/fail
# def pass_function(grade):
#     if grade >40:
#         return "---PASS---"
#     else: 
#         return "---FAIL---" 
# df['pass/fail']=df['percentage'].apply(pass_function)
# df['result']=df['percentage'].apply(pass_function)










# # subject avg




# df['result']
# pass_count=(df['result']=='pass').sum()
# fail_count=(df['result']=='fail').sum()



# # above 80
# above_80=(df['percentage']>-80).sum()

# # below80
# below_80=(df['percentage']<80).sum()


# df.to_csv("C:/Users/acer/OneDrive/Desktop/visco file/tudent Marks Analyzer  start a projects/data/cleanedstudents.csv")

# # chart1
# subject_average=df[subjects].mean()
# plt.figure(figsize=(9,6))
# plt.bar(subject_average.index,subject_average.values)
# plt.title("SUBJECCT AVERAGE")
# plt.xlabel("SUBJECT")
# plt.ylabel("AVERAGE MARKS")
# plt.savefig("C:/Users/acer/OneDrive/Desktop/visco file/tudent Marks Analyzer  start a projects/chart/chart-avg.png")
# plt.show()

## chart2
# plt.figure(figsize=(10,7))
# plt.bar(df['Name'],df['percentage'])
# plt.title("STUDENTS %")
# plt.xlabel("STD NAME")
# plt.ylabel("STD %")
# plt.xticks(rotation=50)
# plt.savefig("C:/Users/acer/OneDrive/Desktop/visco file/tudent Marks Analyzer  start a projects/chart/std%.png")
# plt.show()


#  chart3
# result=df['result'].value_counts()
# plt.figure(figsize=(7,7))
# plt.pie(result.values,labels=result.index,autopct="%1.1f%%")
# plt.title("PASS/FAIL")
# plt.savefig("C:/Users/acer/OneDrive/Desktop/visco file/tudent Marks Analyzer  start a projects/chart/passfail.png")
# plt.show()

# =====================================
# STUDENT PERFORMANCE REPORT
# =====================================

print("\n")
print("=" * 50)
print("       STUDENT PERFORMANCE REPORT")
print("=" * 50)

# topper
topper=df.loc[df['total'].idxmax()]
# topper name
toppername=df.loc[df["total"].idxmax(),"Name"]
topper_percentage = df["percentage"].max()

print("\n🏆 Topper")
print("Name       :", toppername)
print("Percentage :", topper_percentage, "%")


# lower mark
lowest = df.loc[df["percentage"].idxmin()]
lowest_percentage = df["percentage"].min()

print("\n📉 Lowest Scorer")
print("Name       :", lowest)
print("Percentage :", lowest_percentage, "%")
# class avg
class_avg=df['percentage'].mean()
print("\n📊 Class Average")
print("Average :", round(class_avg, 2), "%")
# Pass and Fail
pass_count = (df["result"] == "Pass").sum()
fail_count = (df["result"] == "Fail").sum()

print("\n✅ Passed Students :", pass_count)
print("❌ Failed Students :", fail_count)

# pass pencentage
pass_per=(pass_count/len(df))*100
print("\n🎯 pass pencentage")
print(pass_per)
# topper in each ssubjects
print("\n🥇 Subject Toppers")
for sub in subjects:
    top=df.loc[df[sub].idxmax(),"Name"]
    top_m=df[sub].max()
    print(sub,":",top,"--",top_m)
    # Grade distribution
print("\n🎓 Grade Distribution")

grade_count = df["grade"].value_counts()

print(grade_count)

print("\n")
print("=" * 50)
print("             END OF REPORT")
print("=" * 50)