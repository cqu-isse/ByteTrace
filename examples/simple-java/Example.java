public class Example {
    public static void main(String[] args) {
        System.out.println("RESULT=" + calculate(args.length == 0 ? 3 : Integer.parseInt(args[0])));
    }
    static int calculate(int input) {
        int value = input + 1;
        if (value > 2) {
            value = doubleValue(value);
        } else {
            value = 0;
        }
        return value;
    }
    static int doubleValue(int value) {
        return value * 2;
    }
}
