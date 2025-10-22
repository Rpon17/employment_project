import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'pages/home/bindings/home_binding.dart';
import 'pages/home/views/home_view.dart';

void main() {
  runApp(const SheetProjectApp());
}

class SheetProjectApp extends StatelessWidget {
  const SheetProjectApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: "Bass Sheet App",
      initialBinding: HomeBinding(),
      home: const HomeView(),
      debugShowCheckedModeBanner: false,
    );
  }
}
