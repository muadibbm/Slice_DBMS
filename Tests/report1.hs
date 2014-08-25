import System.IO
import System.Exit
import Data.List.Split
import Data.Char

main = do
	contents <- readFile "SalesDB.schema"
	let schema = splitOn "|" (lines contents !! 0)
	contents <- readFile "SalesDB.slc"
	putStrLn "Cust   Sales"
	let database = lines contents
	putStrLn $ printReport database 0 (getColumnPosition schema 0 "cust") (getColumnPosition schema 0 "total")
	exitSuccess

getColumnPosition :: [String] -> Int -> String -> Int
getColumnPosition database n column
	| length database == n = 0
	| otherwise = do
		if isEqual (map toLower (database !! n)) column (length $ database !! n) (length column) then do n
		else do getColumnPosition database (n+1) column
		
isEqual :: [Char] -> [Char] -> Int -> Int -> Bool
isEqual (x:xs) (y:ys) lenFst lenSnd
	| lenFst == 1 || lenSnd == 1 = True
	| (x == y) = True && isEqual xs ys (lenFst-1) (lenSnd-1)
	| otherwise = False

printReport :: [String] -> Int -> Int -> Int -> String
printReport database n cpos spos
	| length database == n = ""
	| otherwise = do
		((splitOn "|" $ database !! n) !! cpos) ++ "   " ++ ((splitOn "|" $ database !! n) !! spos) ++ "\n" ++ printReport database (n+1) cpos spos