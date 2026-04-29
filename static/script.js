
// // async function loginUser(event) {
// //     event.preventDefault();
// //     const email = document.getElementById('login-email').value;
// //     const password = document.getElementById('login-password').value;

// //     if (!email || !password) {
// //       alert("Please enter both email and password.");
// //       return;
// //     }

// //     try {
// //       const response = await fetch('/login', {
// //         method: 'POST',
// //         headers: {
// //           'Content-Type': 'application/json'
// //         },
// //         body: JSON.stringify({ email, password })
// //       });
  
// //       if (response.redirected) {
// //         // Successful login, redirect to dashboard
// //         window.location.href = response.url;
// //       } else {
// //         const data = await response.json();
// //         if (data.message) {
// //           alert(data.message);  // Shows 'Invalid email or password.' from backend
// //         } else {
// //           alert('Login failed. Please try again.');
// //         }
// //       }
// //     } catch (error) {
// //       console.error('Login error:', error);
// //       alert('User not registered.');
// //     }
// //   }

// async function loginUser(event) {
//   event.preventDefault();

//   const email = document.getElementById('login-email').value.trim();
//   const password = document.getElementById('login-password').value.trim();

//   if (!email || !password) {
//     alert("Please enter both email and password.");
//     return;
//   }

//   try {
//     const response = await fetch('/login', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       credentials: 'include',
//       body: JSON.stringify({ email, password })
//     });

//     if (response.redirected) {
//       // ✅ Backend redirect to /dashboard
//       const redirectUrl = response.url;

//       // 🌟 Optional: store username in localStorage if needed later
//       const user = await response.text();  // Only works if backend returns something, otherwise skip
//       // localStorage.setItem('honeypieUser', JSON.stringify({ name: user }));

//       window.location.href = redirectUrl;
//     } else {
//       const data = await response.json();
//       if (response.ok && data.success) {
//         window.location.href = '/dashboard';  // Manual redirect
//       } else {
//         alert(data.message || 'Login failed.');
// }}
//   } catch (error) {
//     console.error('Login error:', error);
//     alert('Something went wrong. Please try again later.');
//   }
// }
async function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value.trim();

  if (!email || !password) {
    alert("Please enter both email and password.");
    return;
  }

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      const username = data.username;

      // 🌟 Option 1: Store in localStorage (useful across pages)
      // localStorage.setItem('honeypieUser', username);
      localStorage.setItem('honeypieUser', JSON.stringify({ name: username }));

      // 🌟 Option 2: Pass via query string if needed
      window.location.href = `/dashboard?user=${encodeURIComponent(username)}`;
    } else {
      alert(data.message || 'Login failed.');
    }
  } catch (error) {
    console.error('Login error:', error);
    alert('Something went wrong. Please try again later.');
  }
}

