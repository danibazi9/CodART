public class Main {
    public static void main(String[] args) {
        try {
            int[] numbers = new int[]{1, 2, 3};
            int index = 4;
            int i; System
                .out
                .println(numbers[index]); int j; //IndexOutOfBoundsException
        }
        catch (IndexOutOfBoundsException exception){
            System.out.println("IndexOutOfBoundsException Caught...");
            String index = "0";
        }
    }
}