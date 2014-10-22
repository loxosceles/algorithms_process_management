package Tarea_hilos;

/**
 * El programa simula la salida de un carro y el control de esta mediante hilos
 * Reglas de oro del domino(las 3 r's):
 * 1.Respetar la mano
 * 2.Repetir ficha
 * 3.Rechingarse al de la derecha
 * @author Garrido Valencia Alan Rodrigo
 * @author Magnus Henkel
 * @version 1.0 --03/10/2014--
 */
public class Main {
    public String calle="Periferico";
    /**
     * Metodo (hilo)main,que usa a los demas hilos
     * @param args No recibe parametros por linea de comandos
     */
    public static void main(String[] args) {
        System.out.println("Empezando el dia...");
        //Instanciando Objetos
        Auto auto = new Auto("bocho");
        Cochera cochera=new Cochera();
        Trafico trafico=new Trafico(calle);
        Portero portero=new Portero("Jorge Campos");
        //Creando los hilos
        Thread t1 = new Thread(cochera,"hilo2");
        Thread t2 = new Thread(auto,"hilo1");
        Thread t3 = new Thread(trafico, "hilo3");
        //Lanzandolos
        t1.start();
        try {
            //Con join esperamos a que la cochera este abierta para no rayar el auto
            t1.join();
        } catch (InterruptedException iex) {
            System.out.println(iex.getMessage());
        }
        t2.start();
        t3.start();
    }
}
