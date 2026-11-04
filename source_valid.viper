HOLD

# =========================================================
# VIPER STUDENT MANAGEMENT PROGRAM
# =========================================================

fang studentCount = 25;
fang age = 20;
fang marks = 85;

venom average = 87.50;
venom fee = 45000.75;

scale grade = 'A';
scale section = 'B';

coil studentName = "Muhammad Fahad Pervez";
coil university = "University of Karachi";
coil course = "Computer Science";

hiss isEnrolled = true;
hiss hasPassed = false;

# =========================================================
# ARITHMETIC OPERATIONS
# =========================================================

age = age + 1;
marks += 5;
studentCount -= 1;
fee *= 2;
average /= 2;

fang total = marks + age;
fang difference = marks - age;
fang product = marks * age;
fang quotient = marks / age;
fang remainder = marks % age;

# =========================================================
# RELATIONAL OPERATIONS
# =========================================================

hiss adult = age >= 18;
hiss excellent = marks >= 80;
hiss failed = marks < 50;
hiss equalMarks = marks == 85;
hiss differentMarks = marks != 40;
hiss higher = marks > age;
hiss lower = age < marks;

# =========================================================
# LOGICAL OPERATIONS
# =========================================================

hiss eligible = adult && isEnrolled;
hiss rejected = failed || hasPassed;
hiss notPassed = !hasPassed;

# =========================================================
# CONDITIONS
# =========================================================

strike(age >= 18) {

    hissout("Student is an adult");

}

strike(marks >= 80 && isEnrolled) {

    hissout("Student is eligible");

}

strike(marks < 50 || failed) {

    hissout("Student needs improvement");

}

# =========================================================
# NESTED BLOCK
# =========================================================

nest() {

    fang internalMarks = 45;
    fang finalMarks = 40;

    fang totalMarks = internalMarks + finalMarks;

    strike(totalMarks >= 80) {

        hissout("Good performance");

    }

}

# =========================================================
# LOOP / CONTROL KEYWORDS
# =========================================================

strike(turn > 0) {

    turn -= 1;

}

shift(age < 25) {

    age += 1;

}

slither(marks > 0) {

    marks -= 1;

}

coilrun(studentCount > 0) {

    studentCount -= 1;

}

# =========================================================
# ADDITIONAL VIPER KEYWORDS
# =========================================================

sense(marks);

hissout(studentName);

slide;

stalk;

lurk;

escape;

fangback;

# =========================================================
# ARRAY / SYMBOL TESTING
# =========================================================

fang scores[5];

scores[0] = 90;
scores[1] = 85;
scores[2] = 88;

# =========================================================
# MULTIPLE VALUES / SEPARATORS
# =========================================================

fang x = 10, y = 20;

# =========================================================
# MULTILINE COMMENT TEST
# =========================================================

##

This is a multiline comment.

It contains VIPER keywords:
fang venom strike HOLD RELEASE

And operators:
+ - * / % == != <= >= && ||

##

# =========================================================
# FINAL VALUES
# =========================================================

fang finalScore = 95;
venom percentage = 92.75;
scale finalGrade = 'A';
coil message = "VIPER lexical analysis completed";
hiss completed = true;

RELEASE