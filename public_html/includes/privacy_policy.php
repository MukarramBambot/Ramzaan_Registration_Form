<?php
$privacy_policy = [
    "title" => "Privacy Policy",
    "collected_data" => ["name", "phone number", "ITS number"],
    "purpose" => "registration purposes",
    "third_party_sharing" => false,
    "statement" => "Data is not shared with third parties."
];

// Example of how to use it:
echo "<h2>" . $privacy_policy['title'] . "</h2>";
echo "We collect " . implode(", ", $privacy_policy['collected_data']) . " for " . $privacy_policy['purpose'] . ".<br>";
echo $privacy_policy['statement'];
?>