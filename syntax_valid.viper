HOLD

# =========================================================
# VIPER SYNTAX TEST PROGRAM (uses every grammar rule)
# =========================================================

fang studentCount = 25;
fang age;
venom average = 87.50;
scale grade = 'A';
coil studentName = "Muhammad Fahad";
hiss isEnrolled = true;

##
  Multiline comment:
  skipped by the lexer
##

# ---------- input / assignment ----------

sense(age);
age = age + 1;
studentCount -= 1;
average = average * 2 / (age % 3 + 1);
fang a = 1;
fang b = 2;
a = b = 5;

# ---------- conditional ----------

strike (age >= 18 && isEnrolled) {
    hissout("Adult", age);
}
shift (age > 12 || !isEnrolled) {
    hissout("Teen");
}
slither {
    hissout("Child");
}

# ---------- loops ----------

coilrun (fang i = 0; i < studentCount; i += 1) {
    strike (i % 2 == 0) {
        slide;
    }
    hissout(i);
}

stalk (studentCount != 0) {
    studentCount -= 1;
    strike (studentCount <= 3) {
        escape;
    }
}

lurk {
    age = age - 1;
} stalk (age > 0);

# ---------- functions ----------

nest fang add(fang x, fang y) {
    fangback x + y;
}

nest shed greet() {
    hissout("Hello", studentName);
}

RELEASE
