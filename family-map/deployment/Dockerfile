FROM python:3.14.6
# FROM amd64/ubuntu:resolute

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir family_map/
WORKDIR /family_map
COPY lib ./lib
COPY map_family.py .

# COPY deployment/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gspread \ 
pandas \
google-auth \
google-auth-oauthlib \
plotly==6.0.1



# COPY . .

# EXPOSE 8000

# 7. Define the runtime command
CMD ["python3", "map_family.py"]
# ENTRYPOINT [ "sleep", "infinity" ]