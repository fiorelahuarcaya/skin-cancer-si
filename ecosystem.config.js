module.exports = {
  apps: [
    {
      name: "front",
      script: "sirv -p 5000 --cors ../front/dist",
    },
    {
      name: "back",
      script: "python3 ./server.py",
    },
  ],
};
