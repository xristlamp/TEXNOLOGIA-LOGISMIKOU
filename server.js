const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const app = express();
const PORT = 5000;

app.use(bodyParser.json());
app.use(cors());

const getUsers = () => {
  const data = fs.readFileSync('users.json');
  return JSON.parse(data);
};

const saveUsers = (users) => {
  fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
};

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const users = getUsers();
  const user = users.find(u => u.username === username && u.password === password);
  if (user) {
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    user.otp = otp; // Save OTP in user object
    saveUsers(users); // Save the updated users list
    console.log(`OTP for user ${user.username}: ${otp}`); // In a real app, send this via SMS or email
    res.status(200).json({ userId: user.id, role: user.role, message: 'OTP sent' });
  } else {
    res.status(401).json({ message: 'Invalid username or password' });
  }
});

app.post('/api/verify-otp', (req, res) => {
  const { userId, otp } = req.body;
  const users = getUsers();
  const user = users.find(u => u.id === userId && u.otp === otp);
  if (user) {
    delete user.otp; // Remove OTP after verification
    saveUsers(users); // Save the updated users list
    res.status(200).json({ message: 'Login successful' });
  } else {
    res.status(401).json({ message: 'Invalid OTP' });
  }
});

app.post('/api/register', (req, res) => {
  const { username, email, password, role } = req.body;
  const users = getUsers();
  const existingUser = users.find(u => u.username === username || u.email === email);
  if (existingUser) {
    res.status(400).json({ message: 'Username or email already exists' });
  } else {
    const newUser = {
      id: users.length + 1,
      username,
      email,
      password,
      role
    };
    users.push(newUser);
    saveUsers(users);
    res.status(201).json({ message: 'User registered successfully' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
