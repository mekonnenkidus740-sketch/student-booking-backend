import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class BookedStudentPage extends StatefulWidget {
  const BookedStudentPage({super.key});

  @override
  State<BookedStudentPage> createState() => _BookedStudentPageState();
}

class _BookedStudentPageState extends State<BookedStudentPage> {
  List bookings = [];
  bool isLoading = true;

  final String baseUrl =
      "https://student-booking-backend.onrender.com"; // change if needed

  @override
  void initState() {
    super.initState();
    fetchBookings();
  }

  // ================= FETCH BOOKINGS =================
  Future<void> fetchBookings() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/bookings"));

      if (response.statusCode == 200) {
        setState(() {
          bookings = jsonDecode(response.body);
          isLoading = false;
        });
      }
    } catch (e) {
      print(e);
    }
  }

  // ================= DELETE BOOKING =================
  Future<void> deleteBooking(int id) async {
    await http.delete(Uri.parse("$baseUrl/delete_booking/$id"));

    fetchBookings();
  }

  // ================= EDIT BOOKING =================
  void showEditDialog(Map booking) {
    TextEditingController nameController = TextEditingController(
      text: booking['name'],
    );

    TextEditingController dateController = TextEditingController(
      text: booking['date'],
    );

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Edit Booking"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(labelText: "Student Name"),
            ),
            TextField(
              controller: dateController,
              decoration: const InputDecoration(labelText: "Date"),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () async {
              await http.put(
                Uri.parse("$baseUrl/update_booking/${booking['id']}"),
                headers: {"Content-Type": "application/json"},
                body: jsonEncode({
                  "name": nameController.text,
                  "date": dateController.text,
                }),
              );

              Navigator.pop(context);
              fetchBookings();
            },
            child: const Text("Save"),
          ),
        ],
      ),
    );
  }

  // ================= LOGOUT =================
  void logout() {
    Navigator.pushNamedAndRemoveUntil(context, "/login", (route) => false);
  }

  // ================= UI =================
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Booked Students"),
        actions: [
          IconButton(icon: const Icon(Icons.logout), onPressed: logout),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : bookings.isEmpty
          ? const Center(child: Text("No bookings found"))
          : ListView.builder(
              itemCount: bookings.length,
              itemBuilder: (context, index) {
                final booking = bookings[index];

                return Card(
                  margin: const EdgeInsets.all(10),
                  child: ListTile(
                    title: Text(booking['name']),
                    subtitle: Text("Date: ${booking['date']}"),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.edit),
                          onPressed: () => showEditDialog(booking),
                        ),
                        IconButton(
                          icon: const Icon(Icons.delete),
                          onPressed: () => deleteBooking(booking['id']),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
