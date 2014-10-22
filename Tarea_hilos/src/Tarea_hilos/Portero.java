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
public class Portero implements Runnable{
    
    private String nombre;

    public String getNombre() {
        return nombre;
    }

    public Portero(String nombre) {
        this.nombre = nombre;
    }
    
    
    public void abrir(){
        System.out.println("Abriendo");
    }
    @Override
    public void run(){
        try {
            System.out.println(getNombre()+":Abriendo cochera");
            Thread.sleep(5000);
        } catch (InterruptedException iex) { 
            System.out.println(iex.getMessage());
                }
        
    }
}
