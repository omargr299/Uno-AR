                        carta = mazo.Agarrar()
                        carta = mesa.J1.Agregar(carta)
                        sprites.add(carta)
                        mesa.J1.Ordenar()
                        Cambio(False)

                sprites.update(x1,y1,click,(linea[4],linea[5]))
                cv2.circle(frame, (linea[4],linea[5]), 10, (0,255,0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy
            
    fondo = cv2pg(frame