import java.util.LinkedList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numberOfOrder = sc.nextInt();
        String order = "";
        DoublyLinkedList doublyLinkedList = new DoublyLinkedList();
        while (sc.hasNext()) {
            order = sc.next();
            if (order.equals("insert_front")) {
                int value = sc.nextInt();
                System.out.println(doublyLinkedList.insert_front(value));
            }
            if (order.equals("insert_rear")) {
                int value = sc.nextInt();
                System.out.println(doublyLinkedList.insert_rear(value));
            }
            if (order.equals("insert_after_value")) {
                int pre = sc.nextInt();
                int value = sc.nextInt();
                System.out.println(doublyLinkedList.insert_after_value(pre, value));
            }
            if (order.equals("insert_after_index")) {
                int pre = sc.nextInt();
                int value = sc.nextInt();
                System.out.println(doublyLinkedList.insert_after_index(pre, value));
            }
            if (order.equals("delete_value")) {
                int value = sc.nextInt();
                System.out.println(doublyLinkedList.delete_value(value));
            }
            if (order.equals("delete_index")) {
                int index = sc.nextInt();
                System.out.println(doublyLinkedList.delete_index(index));
            }
            if (order.equals("next")) {
                System.out.println(doublyLinkedList.next());
            }
            if (order.equals("previous")) {
                System.out.println(doublyLinkedList.previous());
            }
            if (order.equals("get")) {
                int index = sc.nextInt();
                System.out.println(doublyLinkedList.get(index));
            }
            if (order.equals("front")) {
                System.out.println(doublyLinkedList.front());
            }
            if (order.equals("rear")) {
                System.out.println(doublyLinkedList.rear());
            }
            if (order.equals("clear")) {
                System.out.println(doublyLinkedList.clear());
            }
            if (order.equals("is_empty")) {
                System.out.println(doublyLinkedList.is_empty());
            }
            if (order.equals("size")) {
                System.out.println(doublyLinkedList.size());
            }
        }

    }
}

class DoublyLinkedList {
    int[] list = new int[10000];
    int counter = 0, size = 0;

    DoublyLinkedList() {
        for (int i = 0; i < 10000; i++) {
            list[i] = 0;
        }
    }

    public boolean insert_front(int value) {
        boolean bool = true;
        if (value == 0) bool = false;
        if (list[0] != 0 && value != 0) {
            for (int i = 0; i < size; i++) {
                list[i + 1] = list[i];
            }
            size++;
            list[0] = value;
        }
        if (list[0] == 0 && value != 0) {
            list[0] = value;
            size++;
        }
        return bool;
    }

    public boolean insert_rear(int value) {
        boolean bool = true;
        if (value == 0) bool = false;
        if (value != 0) {
            list[size] = value;
            size++;
        }
        return bool;
    }

    public boolean insert_after_value(int previous, int value) {
        boolean bool = false;
        int pre = 0;
        int a = 0;
        if (value != 0) {
            for (int i = 0; i < size; i++) {
                if (list[i] == previous) {
                    pre = i;
                    a++;
                    bool = true;
                    break;
                }
            }
            if (a != 0) {
                for (int i = size; i > pre; i--) {
                    list[i] = list[i - 1];
                }
                list[pre + 1] = value;
                size++;
            }
        }
        return bool;
    }

    public boolean insert_after_index(int index, int value) {
        boolean bool = false;
        if (value != 0 && index < size && index >= 0) {
            bool = true;
            for (int i = size; i > index; i--) {
                list[i] = list[i - 1];
            }
            list[index + 1] = value;
            size++;
        }

        return bool;
    }

    public boolean delete_value(int value) {
        boolean bool = false;
        int num = 0;
        int a = 0;
        for (int i = 0; i < size; i++) {
            if (list[i] == value) {
                a++;
                bool = true;
                num = i;
                break;
            }
        }
        if (a != 0) {
            for (int i = num; i < size; i++) {
                list[i] = list[i + 1];
            }
            size--;
        }
        return bool;
    }

    public boolean delete_index(int index) {
        boolean bool = false;
        if (index >= 0 && index < size) {
            bool = true;
            for (int i = index; i < size; i++) {
                list[i] = list[i + 1];
            }
            size--;
        }
        return bool;
    }

    public int next() {
        int value = 0;
        if (counter + 1 >= size) value = 0;
        if (counter + 1 < size) {
            counter++;
            value = list[counter];
        }
        return value;
    }

    public int previous() {
        int value = 0;
        if (counter - 1 >= 0) {
            counter--;
            value = list[counter];
        }
        return value;
    }

    public int get(int index) {
        int value = 0;
        if (index >= 0 && index < size) {
            value = list[index];
        }
        return value;
    }

    public int front() {
        int value = 0;
        if (size != 0) value = list[0];
        return value;
    }

    public int rear() {
        int value = 0;
        if (size != 0) value = list[size - 1];
        return value;
    }

    public boolean clear() {
        boolean bool =false;
        if (size != 0) {
            bool=true;
            for (int i = 0; i < size; i++) {
                list[i] = 0;
            }
            size = 0;
        }
        return bool;
    }

    public boolean is_empty() {
        return size == 0;
    }

    public int size() {
        return size;
    }
}

