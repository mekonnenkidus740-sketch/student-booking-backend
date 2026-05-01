import 'package:flutter/material.dart';

class BookStudentPage extends StatelessWidget {
  const BookStudentPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Booking Page")),
      body: const Center(
        child: Text("Student Booking Page", style: TextStyle(fontSize: 20)),
      ),
    );
  }
}
