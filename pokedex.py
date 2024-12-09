import flet as ft 
import flet.canvas as cv
import math 
import aiohttp
import asyncio
#? Variables para el uso de la poke api 
# Antes en local pero ahora en global 
pokemon_actual=0



async def main (page:ft.Page):
  

  page.window_width= 520
  page.window_height= 900
  page.window_resizable=False
  page.padding=0
  page.fonts={
     "zpix":"https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.9/zpix.ttf",
  }
  page.theme = ft.Theme(font_family="zpix")



  
  #? Realizar peticiones a la poke api 
  async def peticion(url):
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        #-- Mejor el formato y permite usar [Name ]abajo 

        return await response.json()
        # Evento vacio en flet se le indica manualmente que debe
  async def get_pokemon(e:ft.ContainerTapEvent):
    global pokemon_actual
    if e.control==arrow_up:
      pokemon_actual+=1
    else:
      pokemon_actual-=1

    numero=(pokemon_actual%150)+1
    resultado= await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")
    datos = f"Name: {resultado['name']}\n\nAbilities:"
    for elemento in resultado['abilities']:
     habilidad= elemento['ability']['name']
     datos += f"\n{habilidad}"
    datos+= f"\n\nHeigth: {resultado['height']}"
    #Print de prueba 
    #    # print(resultado['name'])
    texto.value=datos
    sprite_url=f"https://raw.githubusercontent.com/PokeAPI/sprites/52427d467f3e3b22af3c9cefc807a7452196ccd7/sprites/pokemon/{numero}.png"
    img.src=sprite_url
    await page.update_async()
  
  # ? I sued stack 'cuse
    # - Big buton blue and withe  
  boton_grande=ft.Stack([
    ft.Container(width=80,height=80  ,bgcolor=ft.colors.WHITE ,
    border_radius=50),
    ft.Container(width=70,height=70,left=5,top=3  ,bgcolor=ft.colors.BLUE_700,
    border_radius=50)
    
  ])
  #? Small circles 
  items_superior=[
   ft.Container( boton_grande,width=80,height=80   ),
   ft.Container(width=40,height=40   ,bgcolor=ft.colors.GREEN,
    border_radius=50),
   ft.Container(width=40,height=40   ,bgcolor=ft.colors.YELLOW,
    border_radius=50),
   ft.Container(width=40,height=40   ,bgcolor=ft.colors.BLUE,
    border_radius=50)
   ]
  #? Img 
  sprite_url=f"https://raw.githubusercontent.com/PokeAPI/sprites/52427d467f3e3b22af3c9cefc807a7452196ccd7/sprites/pokemon/0.png"
  img=ft.Image(
     src=sprite_url,
     scale=10,
     width=20,
     height=20,
     left=220,
     bottom=5,
     top=5
     
   )
  stack_central=ft.Stack([
    #? white box 
     ft.Container(width= 450,height=400  ,bgcolor=ft.colors.WHITE,border_radius=20
    ),
    #? Black box
     ft.Container(width=325,height=150  ,bgcolor=ft.colors.BLACK,
   top=25,left=65 ),
   #
   img
  ])
  tringle=cv.Canvas([
    cv.Path([
      cv.Path.MoveTo(40,0),
      cv.Path.LineTo(0,50),
      cv.Path.LineTo(80,50),

    ])

  ])
  #? Solo se extrea uno por que usamos sol un if else  ver line 29
  arrow_up= ft.Container(tringle,width=80,height=75,on_click=get_pokemon )
  Up_Down=ft.Column([
    #ft.Container(tringle,width=80,height=75,on_click=get_pokemon )
    # Se uso para pribar funcionalidad 
    arrow_up,
    #? Para evitar el crear otro trinagulo solo lo roto 
    #-- Esta en radines el triangulo y se rota en angulos 

    ft.Container(tringle,rotate=ft.Rotate(angle=math.radians(180) ), width=80,height=75 ,on_click=get_pokemon ),
   
  ])
  #-- Texto informativo 
  texto=ft.Text(
    
    value="",
    color=ft.colors.BLACK,
    size=15,
    
  )
  items_inferior=[
  ft.Container( width=50     ),
  ft.Container(texto,width=300,height=150,bgcolor=ft.colors.GREEN,border_radius=20),
  ft.Container(Up_Down,width=80,height=150  ),
  ft.Container( width=50     ),
 
   ]



  #? Superior margin
  superior=ft.Container(content=ft.Row(items_superior),width= 510,height=80,margin=ft.margin.only(top=40)  )
  #? Mid margin 
  mid=ft.Container(content=stack_central,width= 510,height=200,margin=ft.margin.only(top=40)  ,alignment=ft.alignment.center)
  #? Buttom margin
  inferior=ft.Container(content=ft.Row(items_inferior),width= 510,height=200,margin=ft.margin.only(top=40)  )


  col=ft.Column(spacing=0,controls=[
    superior,
    mid,
    inferior
  ])

  #? Red container 
  contenedor=ft.Container(col,width=520,height=900,bgcolor=ft.Colors.RED,alignment=ft.alignment.top_center)
  await page.add_async(contenedor)




ft.app(target=main)

