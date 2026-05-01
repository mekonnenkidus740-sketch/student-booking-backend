import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class GoogleAuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn();

  Future<String?> signIn() async {
    try {
      final GoogleSignInAccount? user = await _googleSignIn.signIn();

      if (user == null) {
        return null;
      }

      String email = user.email;
      String name = user.displayName ?? "";

      var response = await http.post(
        Uri.parse("https://student-booking-backend.onrender.com/google-login"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"name": name, "email": email}),
      );

      if (response.statusCode == 200) {
        return email;
      } else {
        return null;
      }
    } catch (e) {
      print(e);
      return null;
    }
  }
}
