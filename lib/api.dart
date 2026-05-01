class Api {
  static const String baseUrl =
      "https://student-booking-backend.onrender.com"; // Your PC IP
  static String get register => "$baseUrl/register";
  static String get login => "$baseUrl/login";
  static String get logout => "$baseUrl/logout"; // Optional
  static String get addStudent => "$baseUrl/add_student"; // Optional
  static String get getStudents => "$baseUrl/students";
  static String get updateStudent => "$baseUrl/update_student";
  static String get deleteStudent => "$baseUrl/delete_student";
}
