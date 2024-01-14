import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Desativar a observação de arquivos para o Streamlit no Docker
# st.set_option('server.headless', True)

# Chave de API da OpenWeatherMap (substitua pela sua chave)
API_KEY = ""

def obter_previsao_tempo(cidade):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" para Fahrenheit ou "metric" para Celsius
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
        return (dados_clima['coord']['lat'], dados_clima['coord']['lon'])
    else:
        st.warning("Insira uma cidade válida.")
        return None

def exibir_mapa(latitude, longitude):
    st.write("**Mapa da Cidade**")
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker(location=[latitude, longitude], popup="Cidade").add_to(m)
    folium_static(m)

def main():
    st.title("Aplicativo de Previsão do Tempo e Mapa")

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




