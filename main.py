import psutil
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def get_cpu_usage():
    # Returns CPU usage percentage over a 1-second interval
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    ram = psutil.virtual_memory()
    total_gb = ram.total / (1024 ** 3)
    used_gb = ram.used / (1024 ** 3)
    percent = ram.percent
    return total_gb, used_gb, percent


def get_disk_usage():
    disk = psutil.disk_usage("/")
    total_gb = disk.total / (1024 ** 3)
    used_gb = disk.used / (1024 ** 3)
    percent = disk.percent
    return total_gb, used_gb, percent


def build_table(cpu, ram, disk):
    table = Table(
        title="System Monitor",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Resource", style="bold white", width=12)
    table.add_column("Usage", justify="right", width=10)
    table.add_column("Details", width=30)

    # CPU row — colour changes based on load
    cpu_color = "green" if cpu < 50 else "yellow" if cpu < 80 else "red"
    table.add_row(
        "CPU",
        f"[{cpu_color}]{cpu:.1f}%[/{cpu_color}]",
        f"[{cpu_color}]{'█' * int(cpu / 5)}[/{cpu_color}]",
    )

    # RAM row
    ram_total, ram_used, ram_percent = ram
    ram_color = "green" if ram_percent < 60 else "yellow" if ram_percent < 85 else "red"
    table.add_row(
        "RAM",
        f"[{ram_color}]{ram_percent:.1f}%[/{ram_color}]",
        f"{ram_used:.1f} GB used of {ram_total:.1f} GB",
    )

    # Disk row
    disk_total, disk_used, disk_percent = disk
    disk_color = "green" if disk_percent < 70 else "yellow" if disk_percent < 90 else "red"
    table.add_row(
        "Disk",
        f"[{disk_color}]{disk_percent:.1f}%[/{disk_color}]",
        f"{disk_used:.1f} GB used of {disk_total:.1f} GB",
    )

    return table


def main():
    console.print("\n[bold cyan]Collecting system information...[/bold cyan]\n")

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()

    table = build_table(cpu, ram, disk)
    console.print(table)
    console.print()


if __name__ == "__main__":
    main()
