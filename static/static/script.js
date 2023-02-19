/* Função para enviar dados do formulário para a API */

async function submitData() {
  const name = document.getElementById("name").value;
  const gender = document.getElementById("gender").value;
  const cpf = document.getElementById("cpf").value;
  const rg = document.getElementById("rg").value;
  const address = document.getElementById("address").value;
  const maritalStatus = document.getElementById("marital_status").value;
  const balance = document.getElementById("balance").value;
  const loan = document.getElementById("loan").value;
  const creditCard = document.getElementById("credit_card").value;
  const income = document.getElementById("income").value;
  
  const response = await fetch("/api/v1/clients/", {
  method: "POST",
  headers: {
  "Content-Type": "application/json",
  },
  body: JSON.stringify({
  name,
  gender,
  cpf,
  rg,
  address,
  marital_status: maritalStatus,
  balance,
  loan: loan === "True",
  credit_card: creditCard === "True",
  income,
  }),
  });
  
  if (response.ok) {
  alert("Cliente cadastrado com sucesso!");
  } else {
  alert("Ocorreu um erro ao cadastrar o cliente.");
  }
  }
  
  /* Funções para a página de login */
  
  const loginForm = document.getElementById("login-form");
  const loginError = document.getElementById("login-error");
  
  loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  
  const response = await fetch("/api/v1/login/", {
  method: "POST",
  headers: {
  "Content-Type": "application/json",
  },
  body: JSON.stringify({ username, password }),
  });
  
  if (response.ok) {
  const data = await response.json();
  localStorage.setItem("token", data.token);
  window.location.href = "/dashboard";
  } else {
  loginError.innerHTML = "Usuário ou senha inválidos.";
  }
  });
  
  /* Função para fazer logout */
  
  const logoutButton = document.getElementById("logout-button");
  
  logoutButton.addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.removeItem("token");
  window.location.href = "/";
  });