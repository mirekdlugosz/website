Title: Understanding Linux virtualization stack
Slug: understanding-linux-virtualization-stack
Date: 2024-11-12 23:37:46
Category: Blog
Tags: Linux, planet AST, planet MoT, planet Python


I find Linux virtualization stack confusing. KVM? libvirt? QEMU? Xen? What does that even mean?

This post is my attempt at making sense of that all. I don't claim it to be correct, but that's the way I understand it. If I badly missed a mark somewhere, please [reach out and tell me how wrong I am]({filename}/pages/contact.md).

## Virtualization primer

Virtual machine is a box inside which programs think they are running on different hardware and operating system. That box is like a full computer, running inside a computer. Virtualization is process of creating these boxes. Virtual machine is called guest, while operating system that runs virtual machine is called host.

Two main reasons to virtualize are security and resource management. Security - because if virtual machine is done correctly, then program inside it won't even know it's inside a virtual machine, and that means there's a good chance it won't escape to interfere with other programs. Resource management - so you can buy huge server and assign slice of resources to each box as you see fit, and dynamically change it as your needs shift.

Virtual machine pretends to be the entire computer, but most discussions revolve around CPU. Each CPU architecture has a specific set of instructions, and programs generally target only one of them. It is technically possible to translate instructions from one architecture to another, but that's usually slow. Most modern CPUs provide extensions that allow virtual machines to run at speed comparable to non-virtualized installations. Using these extensions is only possible when the guest and the host target the same CPU architecture.

Conceptually, there is no significant difference between virtualization and emulation. Practically, emulation usually refers to guest thinking it has different CPU architecture than host, and to virtual machine pretending to be some very specific physical hardware - like a video game console. Virtualization in turn usually refers to specific case where guest thinks it has the same CPU architecture as the host.

## KVM

KVM is part of the kernel, responsible for talking with hardware. As I mentioned before, most modern CPUs have special extensions that allow guests to achieve near-native performance. KVM makes it possible for Linux host to use these extensions.

## QEMU

QEMU is weird, because it's multiple different things.

First, it can run virtual machines and pass instructions from guest to KVM, where they will be handled by virtualization CPU extension. So you can think about QEMU as user space component for KVM.

Second, it can run virtual machines while emulating different CPU architecture. So you can think about QEMU as user space virtualization solution, which can run without KVM at all.

Third, it can run programs targeting one CPU architecture on a computer with another CPU architecture. It's like lightweight virtualization, where only single program is virtualized.

Finally, it is set of standalone utilities related to virtualization, but not directly tied to anything in particular. Most of these programs work with disk image files in some way.

QEMU is probably the hardest part to understand, because it can do things that other parts of the stack are responsible for. This results in some overlap between different components and encountering program names in contexts where you would not expect them.

I _think_ this overlap is mostly a historical artifact. The oldest commit in QEMU git repository is dated 2003, while KVM was included in Linux kernel in 2007. So it seems to me that QEMU was originally intended as software virtualization solution that did not depend on any hardware or kernel driver. Later Linux gained drivers for virtualization CPU extensions, but they were useless without something in user space that could work with them. So instead of creating completely new thing, QEMU was extended to work with KVM.

Technically, the journey towards understanding Linux virtualization stack could end here - you _can_ use QEMU to create, start, stop and modify virtual machines. But QEMU commands tend to be verbose and long, so people rarely use it directly.

## libvirt

I have ignored that so far, but KVM is not the only virtualization driver in kernel. There are many, some of them closed-source.

libvirt is intended as unified layer that abstracts virtual machine management for application developers. So if you would like your application to create, start, stop or delete virtual machine, you don't have to support each of these operations on KVM, QEMU, Xen and VirtualBox - you can just support libvirt and trust it will do the right thing.

libvirt doesn't do any work directly, and instead asks other programs to do it. System administrator is responsible for setting up the host and ensuring virtualization may work. This makes libvirt great for application developers, who can forget about details of different solutions; but most of libvirt users are in less fortunate position, because they have to take a role of system administrator.

libvirt will talk with QEMU, which in turn may pass CPU instructions to KVM. Some sources online claim that libvirt can talk with KVM directly. libvirt itself perpetuates this confusion, as KVM is listed alongside QEMU on the main page, giving the impression they are two equivalent components. But detailed documentation page makes it clear - libvirt only talks with QEMU. It can detect KVM and allow user to create "hardware accelerated guests", but that case is still handled through QEMU.

It's also worth noting that libvirt supports multiple virtualization drivers across multiple operating systems, including FreeBSD and macOS.

## virsh

virsh is a command line interface for libvirt. That's it, there's nothing more to it. If it was created today, it might have been called libvirtctl.

## Vagrant

Vagrant abstracts virtual machine management across operating systems. It's similar to libvirt, in the way that it allows application developers to target Vagrant and leave all the details to someone else. And just like libvirt, Vagrant doesn't do anything on its own, but pushes all the work to tools lower in the stack.

Vagrant primary audience is software developers. It allows to succinctly define multiple virtual machines, and then start and provision them all with a single command. These machines are usually considered disposable - they might be deleted and re-created multiple times a day. If you want to manually modify the virtual machine and keep these changes for longer period of time, Vagrant is probably not a tool for you.

On Linux, Vagrant usually works with libvirt, but may also work with VirtualBox or Xen.

## VirtualBox

VirtualBox is full virtualization solution. It consists of kernel driver and user space programs, including one with graphical interface. You can think of VirtualBox as something parallel to all that we've discussed so far.

The main reason to use VirtualBox is ease of use. It offers simpler mental model for virtualization - you just install VirtualBox, start VirtualBox UI and create and run virtual machines. While it does require a kernel module, and kernel is notoriously bad at breaking modules that are not in tree, VirtualBox has a lot of tooling and integrations that will ensure that module is built every time you install or update kernel image. On distributions like Ubuntu you don't have to think about this at all.

Technically speaking, libvirt supports VirtualBox, so you can use libvirt and virsh to manage VirtualBox machines. In practice that seems to be rare.

## Xen

Xen is another virtualization stack. You can think about it as something parallel to KVM/QEMU/libvirt and VirtualBox. What sets Xen apart is that instead of running _inside_ your operating system, it runs _below_ your operating system.

Xen manages scheduling, interrupts and timers - that is, it manages who gets access to computer resources, when, and for how long. Xen is the very first thing that starts when you boot your computer.

But Xen is not an operating system. So right after starting, it starts the guest with one. That guest is special, because it provides drivers to hardware and is the only one with a privilege to talk with Xen. Only through that special guest virtual machine you can create other virtual machines, assign them resources etc.

Xen is one of the oldest virtualization solutions, with first release back in 2003. However, it was included in kernel only in 2010. So while many people prefer Xen and think favorably of its architecture, it seems to lost the popularity contest to KVM and QEMU.

Xen provides the tools required to manage guest virtual machines, but you can also manage them through libvirt.

## Summary

I thought to put a visual aid in place of summary. Each column represents a possible stack - you generally want to pick one of them. Items with dashed line style are optional - you can use them, but don't have to. Click to see the bigger image.

{% figure
    {attach}linux-virtualization-stack/linux-virtualization-stack.jpg |
    caption=Overview of possible Linux virtualization stacks
%}
