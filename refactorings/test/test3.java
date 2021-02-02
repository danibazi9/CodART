public class Main {
    public static void main(String[] args) {

        int[] numbers = new int[]{1, 2, 3};
        int index = 4;
        int i;
        if (index < numbers.length) {
            System
                    .out
                    .println(numbers[index]); }
        else {
            System.out.println("IndexOutOfBoundsException Caught...");
            String index = "0";
        }
        int j; //IndexOutOfBoundsException
    }
}