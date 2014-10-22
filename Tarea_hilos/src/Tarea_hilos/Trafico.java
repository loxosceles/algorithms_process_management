/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Tarea_hilos;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Guillermo Garr1d0
 */
public class Trafico implements Runnable{

    private String calle;
    
    public Trafico(String calle) {
        this.calle = calle;
    }
    
    
    @Override
    public void run(){
        synchronized(calle){
            try {   
                System.out.println("Ahora hay trafico en: "+calle);
            
                Thread.sleep((long)(Math.random() * 10000));
                notify();
            } catch (InterruptedException iex) {
                System.out.println(iex.getMessage());
            }
        }
    }
}
