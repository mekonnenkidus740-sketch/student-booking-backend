import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'home_page.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final TextEditingController firstController = TextEditingController();
  final TextEditingController lastController = TextEditingController();
  final TextEditingController inputController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  bool isLoading = false;

  Future<void> register() async {
    String first = firstController.text.trim();
    String last = lastController.text.trim();
    String input = inputController.text.trim();
    String password = passwordController.text.trim();

    if (first.isEmpty || last.isEmpty || input.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("All fields are required")));
      return;
    }

    setState(() => isLoading = true);

    try {
      print("Sending register request...");

      final response = await http.post(
        Uri.parse("https://student-booking-backend.onrender.com/register"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "firstName": first,
          "lastName": last,
          "input": input,
          "password": password,
        }),
      );

      print("Status: ${response.statusCode}");
      print("Response: ${response.body}");

      if (!mounted) return;

      final data = jsonDecode(response.body);

      if (response.statusCode == 201) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => HomePage(
              firstName: first,
              lastName: last[0] + "*" * (last.length - 1),
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(data["message"])));
      }
    } catch (e) {
      print("ERROR: $e");
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Connection error")));
    }

    setState(() => isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              children: [
                const Text("Register", style: TextStyle(fontSize: 26)),
                const SizedBox(height: 20),

                TextField(
                  controller: firstController,
                  decoration: const InputDecoration(labelText: "First Name"),
                ),

                const SizedBox(height: 10),

                TextField(
                  controller: lastController,
                  decoration: const InputDecoration(labelText: "Last Name"),
                ),

                const SizedBox(height: 10),

                TextField(
                  controller: inputController,
                  decoration: const InputDecoration(
                    labelText: "Email or Username",
                  ),
                ),

                const SizedBox(height: 10),

                TextField(
                  controller: passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(labelText: "Password"),
                ),

                const SizedBox(height: 25),

                ElevatedButton(
                  onPressed: isLoading ? null : register,
                  child: isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Register"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
