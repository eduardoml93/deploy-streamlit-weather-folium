import streamlit as st
import requests
import folium
import urllib.parse
from streamlit_folium import folium_static

# Desativar a observação de arquivos para o Streamlit no Docker
# st.set_option('server.headless', True)

# Chave de API da OpenWeatherMap (substitua pela sua chave)
API_KEY = "a5676ce9dbe81f9ddad2125c4dedb9b6"

def obter_previsao_tempo(cidade):
    endpoint = "http://api.openweathermap.org/data/2.5/weather&lang=pt_br"
    lang_param = urllib.parse.quote_plus("&lang=pt_br")
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",  # Use "imperial" para Fahrenheit ou "metric" para Celsius
        "extra_param": f"{lang_param}"  # Este é apenas um exemplo de como incluir o parâmetro 'lang'.
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        dados_clima = response.json()
        return dados_clima
    else:
        st.error(f"Erro ao obter dados de previsão do tempo. Código de status: {response.status_code}")
        return None

def exibir_previsao_tempo(dados_clima):
    if dados_clima:
        st.write(f"**Cidade:** {dados_clima['name']}")
        st.write(f"**País:** {dados_clima['sys']['country']}")
        st.write(f"**Temperatura Atual:** {dados_clima['main']['temp']}°C")
        st.write(f"**Tempo:** {dados_clima['weather'][0]['description'].capitalize()}")
        return (dados_clima['coord']['lat'], dados_clima['coord']['lon'], dados_clima)
    else:
        st.warning("Insira uma cidade válida.")
        return None

def exibir_mapa(latitude, longitude, dados_clima):
    st.write("**Mapa da Cidade**")
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # Criar o conteúdo do pop-up sem folium.Popup
    pop_up_content = f"""
    <b>Cidade:</b> {dados_clima['name']}<br>
    <b>País:</b> {dados_clima['sys']['country']}<br>
    <b>Temperatura Atual:</b> {dados_clima['main']['temp']}°C<br>
    <b>Tempo:</b> {dados_clima['weather'][0]['description'].capitalize()}
    """

    # Adicionar o marcador com o conteúdo do pop-up
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(folium.Html(pop_up_content, script=True)),
        icon=folium.Icon(color='blue')
    ).add_to(m)

    folium_static(m)

def main():
    st.title("App de Previsão do Tempo e Mapa")

    # Inserir o nome da cidade
    cidade = st.text_input("Digite o nome da cidade:")

    # Botão para obter a previsão do tempo
    if st.button("Obter Previsão do Tempo"):
        if cidade:
            dados_clima = obter_previsao_tempo(cidade)
            coordenadas = exibir_previsao_tempo(dados_clima)
            if coordenadas:
                exibir_mapa(*coordenadas)

        else:
            st.warning("Insira o nome da cidade para obter a previsão do tempo.")

if __name__ == "__main__":
    main()
