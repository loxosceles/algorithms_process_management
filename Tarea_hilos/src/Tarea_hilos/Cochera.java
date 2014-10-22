package Tarea_hilos;

public class Cochera extends Thread {
    
    @Override
    public void run(){
        
        try {
            System.out.println(getName()+":Abriendo cochera");
            //La cochera tarda 5 segundos en abrir
            Thread.sleep(5000);
            System.out.println("Cochera abierta");
        } catch (InterruptedException iex) { 
            System.out.println(iex.getMessage());
                }
        
    }
}
