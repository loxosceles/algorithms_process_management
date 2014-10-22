/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Tarea_hilos;

/**
 *
 * @author Guillermo Garr1d0
 */
public class Auto extends Thread{
    
    private String nombre;

    public String getNombre() {
        return nombre;
    }
    private String calle;

    public Auto(String nombre) {
        this.nombre = nombre;
    }
    
    public synchronized void conducir(String calle){
        System.out.println("Listo para salir a"+calle);
    }
    public synchronized void regresar(String calle){
        System.out.println("Listo para regresar de "+calle);
    }
    
    @Override
    public void run(){
        
    String hilo = Thread.currentThread().getName();
        System.out.println(hilo+getNombre()+" auto arranco");
        try {
                conducir(calle);
                //Tardamos 10 segundos porque el Periferico esta lleno y queremos regresar
                Thread.sleep(10000);
        } catch (InterruptedException iex) {
            System.out.println(iex.getMessage());
        }
    }   
}
