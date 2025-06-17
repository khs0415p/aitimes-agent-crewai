from crew import NewsCrew


def main():
    crew = NewsCrew().crew()

    results = crew.kickoff()


if __name__ == "__main__":
    main()

