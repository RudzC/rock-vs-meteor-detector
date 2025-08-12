docker build -t meteor-rock:latest .

docker run --rm -p 4000:4000 --name meteor-rock meteor-rock:latest