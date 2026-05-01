import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class BookingPage extends StatelessWidget {
  const BookingPage({super.key});

  Future<void> logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove("user_id");
    Navigator.pushReplacementNamed(context, "/");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Booking Page"),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => logout(context),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () {
                print("Add booking clicked");
              },
              child: const Text("Add Booking"),
            ),
          ],
        ),
      ),
    );
  }
}

void editBooking(Map<String, dynamic> booking) {
  // later
}
