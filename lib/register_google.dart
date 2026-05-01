import 'package:flutter/material.dart';
import 'home_page.dart';

class RegisterPageWithGoogle extends StatefulWidget {
  final String firstName;
  final String lastName;
  final String email;

  const RegisterPageWithGoogle({
    super.key,
    required this.firstName,
    required this.lastName,
    required this.email,
  });

  @override
  State<RegisterPageWithGoogle> createState() => _RegisterPageWithGoogleState();
}

class _RegisterPageWithGoogleState extends State<RegisterPageWithGoogle> {
  void completeRegistration() {
    // Save to backend if needed
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) =>
            HomePage(firstName: widget.firstName, lastName: widget.lastName),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Register with Google", style: TextStyle(fontSize: 26)),
            const SizedBox(height: 20),
            Text("Name: ${widget.firstName} ${widget.lastName}"),
            Text("Email: ${widget.email}"),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: completeRegistration,
              child: const Text("Complete Registration"),
            ),
          ],
        ),
      ),
    );
  }
}
