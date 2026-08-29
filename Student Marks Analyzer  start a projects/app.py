from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    abort,
    send_file
)


import pandas as pd
import os
import matplotlib.pyplot as plt


app = Flask(__name__)


# ==========================================
# FOLDERS
# ==========================================

UPLOAD_FOLDER = "uploads"
CHART_FOLDER = "charts"
OUTPUT_FOLDER = "output"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================
# PROCESS STUDENT DATA
# ==========================================

def process_data(file_path):

    df = pd.read_csv(file_path)

    subjects = [
        "Python",
        "SQL",
        "Java",
        "Maths"
    ]

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    for subject in subjects:

        if subject in df.columns:

            df[subject] = pd.to_numeric(
                df[subject],
                errors="coerce"
            )

            df[subject] = df[subject].fillna(
                df[subject].mean()
            )

    # Total
    df["Total"] = df[subjects].sum(axis=1)

    # Average
    df["Average"] = df[subjects].mean(axis=1)

    # Percentage
    df["Percentage"] = (
        df["Total"] /
        (len(subjects) * 100)
    ) * 100

    df["Average"] = df["Average"].round(2)
    df["Percentage"] = df["Percentage"].round(2)


    # ==========================================
    # GRADE
    # ==========================================

    def calculate_grade(percentage):

        if percentage >= 90:
            return "A+"

        elif percentage >= 80:
            return "A"

        elif percentage >= 70:
            return "B"

        elif percentage >= 60:
            return "C"

        elif percentage >= 50:
            return "D"

        else:
            return "F"


    # ==========================================
    # RESULT
    # ==========================================

    def calculate_result(percentage):

        if percentage >= 40:
            return "Pass"

        return "Fail"


    df["Grade"] = df["Percentage"].apply(
        calculate_grade
    )

    df["Result"] = df["Percentage"].apply(
        calculate_result
    )

    return df, subjects


# ==========================================
# CREATE CHARTS
# ==========================================

def create_charts(df, subjects):

    # ------------------------------------------
    # Subject Average
    # ------------------------------------------

    subject_average = df[subjects].mean()

    plt.figure(figsize=(8, 5))

    plt.bar(
        subject_average.index,
        subject_average.values
    )

    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_FOLDER,
            "subject_average.png"
        )
    )

    plt.close()


    # ------------------------------------------
    # Student Percentage
    # ------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.bar(
        df["Name"],
        df["Percentage"]
    )

    plt.title("Student Percentage")
    plt.xlabel("Students")
    plt.ylabel("Percentage")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_FOLDER,
            "student_percentage.png"
        )
    )

    plt.close()


    # ------------------------------------------
    # Pass / Fail
    # ------------------------------------------

    result_count = df["Result"].value_counts()

    plt.figure(figsize=(6, 6))

    plt.pie(
        result_count.values,
        labels=result_count.index,
        autopct="%1.1f%%"
    )

    plt.title("Pass vs Fail")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_FOLDER,
            "pass_fail.png"
        )
    )

    plt.close()


# ==========================================
# SAVE ANALYSIS
# ==========================================

def save_analysis(df):

    # Create analyzed CSV

    csv_path = os.path.join(
        OUTPUT_FOLDER,
        "analyzed_students.csv"
    )

    df.to_csv(
        csv_path,
        index=False
    )


    # Create analyzed Excel

    excel_path = os.path.join(
        OUTPUT_FOLDER,
        "analyzed_students.xlsx"
    )

    df.to_excel(
        excel_path,
        index=False
    )


    # ==========================================
    # REPORT
    # ==========================================

    total_students = len(df)

    topper = df.loc[
        df["Percentage"].idxmax(),
        "Name"
    ]

    class_average = round(
        df["Percentage"].mean(),
        2
    )

    pass_count = (
        df["Result"] == "Pass"
    ).sum()

    fail_count = (
        df["Result"] == "Fail"
    ).sum()

    pass_percentage = round(
        (pass_count / total_students) * 100,
        2
    )


    report_path = os.path.join(
        OUTPUT_FOLDER,
        "performance_report.txt"
    )


    with open(
        report_path,
        "w"
    ) as file:

        file.write(
            "STUDENT PERFORMANCE REPORT\n"
        )

        file.write(
            "=" * 40 + "\n\n"
        )

        file.write(
            f"Total Students: {total_students}\n"
        )

        file.write(
            f"Topper: {topper}\n"
        )

        file.write(
            f"Class Average: {class_average}%\n"
        )

        file.write(
            f"Passed Students: {pass_count}\n"
        )

        file.write(
            f"Failed Students: {fail_count}\n"
        )

        file.write(
            f"Pass Percentage: {pass_percentage}%\n"
        )


# ==========================================
# HOME
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Check file

        if "file" not in request.files:

            return "No file selected"


        file = request.files["file"]


        if file.filename == "":

            return "No file selected"


        # Check CSV

        if not file.filename.lower().endswith(".csv"):

            return "Please upload a CSV file"


        # ==========================================
        # SAVE UPLOADED FILE
        # ==========================================

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(file_path)


        # ==========================================
        # PROCESS UPLOADED FILE
        # ==========================================

        df, subjects = process_data(
            file_path
        )


        # ==========================================
        # CREATE CHARTS
        # ==========================================

        create_charts(
            df,
            subjects
        )


        # ==========================================
        # SAVE ANALYSIS
        # ==========================================

        save_analysis(df)


        # ==========================================
        # STATISTICS
        # ==========================================

        total_students = len(df)


        topper = df.loc[
            df["Percentage"].idxmax(),
            "Name"
        ]


        class_average = round(
            df["Percentage"].mean(),
            2
        )


        pass_count = (
            df["Result"] == "Pass"
        ).sum()


        fail_count = (
            df["Result"] == "Fail"
        ).sum()


        pass_percentage = round(
            (pass_count / total_students) * 100,
            2
        )


        # ==========================================
        # SHOW DASHBOARD
        # ==========================================

        return render_template(
            "index.html",

            show_result=True,

            total_students=total_students,

            topper=topper,

            class_average=class_average,

            pass_count=pass_count,

            fail_count=fail_count,

            pass_percentage=pass_percentage,

            students=df.to_dict(
                "records"
            )
        )


    # GET request

    return render_template(
        "index.html",
        show_result=False
    )


# ==========================================
# STUDENT DETAILS
# ==========================================

@app.route("/student/<name>")
def student_details(name):

    # Find uploaded CSV files

    files = os.listdir(
        app.config["UPLOAD_FOLDER"]
    )


    csv_files = [

        file

        for file in files

        if file.lower().endswith(".csv")

    ]


    if not csv_files:

        return "Please upload a CSV file first"


    # Get latest uploaded file

    latest_file = max(

        csv_files,

        key=lambda file:
        os.path.getmtime(

            os.path.join(
                app.config["UPLOAD_FOLDER"],
                file
            )

        )

    )


    file_path = os.path.join(

        app.config["UPLOAD_FOLDER"],

        latest_file

    )


    # Process latest uploaded CSV

    df, subjects = process_data(
        file_path
    )


    # Find student

    student_data = df[

        df["Name"]
        .astype(str)
        .str.lower()

        == name.lower()

    ]


    if student_data.empty:

        abort(404)


    student = student_data.iloc[0]


    return render_template(

        "student.html",

        student=student,

        subjects=subjects

    )


# ==========================================
# SERVE CHARTS
# ==========================================

@app.route("/charts/<filename>")
def charts(filename):

    return send_from_directory(

        CHART_FOLDER,

        filename

    )


# ==========================================
# DOWNLOAD CSV
# ==========================================

@app.route("/download/csv")
def download_csv():

    return send_file(

        os.path.join(
            OUTPUT_FOLDER,
            "analyzed_students.csv"
        ),

        as_attachment=True

    )


# ==========================================
# DOWNLOAD EXCEL
# ==========================================

@app.route("/download/excel")
def download_excel():

    return send_file(

        os.path.join(
            OUTPUT_FOLDER,
            "analyzed_students.xlsx"
        ),

        as_attachment=True

    )


# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.route("/download/report")
def download_report():

    return send_file(

        os.path.join(
            OUTPUT_FOLDER,
            "performance_report.txt"
        ),

        as_attachment=True

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

