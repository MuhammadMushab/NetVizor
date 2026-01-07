import subprocess, re
from django.shortcuts import render
from collections import Counter

SCAN_HISTORY = []

def dashboard(request):
    results = []
    error = ""
    target = ""
    scan_type = ""
    ports = ""

    if request.method == "POST":
        target = request.POST.get("target")
        scan_type = request.POST.get("scan_type")
        ports = request.POST.get("ports")

        command = ["nmap"]

        if scan_type == "quick":
            command.append("-F")
        elif scan_type == "full":
            command.append("-p-")
        elif scan_type == "stealth":
            command.append("-sS")
        elif scan_type == "custom" and ports:
            command.extend(["-p", ports])

        command.append(target)

        try:
            p = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if p.returncode != 0:
                error = p.stderr
            else:
                for line in p.stdout.splitlines():
                    m = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)", line)
                    if m:
                        port, proto, service = m.groups()
                        results.append({
                            "host": target,
                            "proto": proto,
                            "port": port,
                            "state": "open",
                            "service": service
                        })

                # Prepare data for charts
                labels = [r['port'] for r in results]
                values = [1] * len(results)  # For bar chart, each port counts as 1

                # For pie chart, protocol distribution
                proto_counts = Counter(r['proto'] for r in results)
                pie_labels = list(proto_counts.keys())
                pie_values = list(proto_counts.values())

                SCAN_HISTORY.append({
                    "target": target,
                    "count": len(results),
                    "type": scan_type or "normal"
                })

        except FileNotFoundError:
            error = "Nmap is not installed or not added to PATH."

    return render(request, "dashboard.html", {
        "results": results,
        "error": error,
        "target": target,
        "history": SCAN_HISTORY[-5:],
        "labels": labels if 'labels' in locals() else [],
        "values": values if 'values' in locals() else [],
        "pie_labels": pie_labels if 'pie_labels' in locals() else [],
        "pie_values": pie_values if 'pie_values' in locals() else []
    })
